# video_agent_service_final.py
import os
import re
from typing import TypedDict, List, Dict, Any, Optional

from langdetect import detect
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from services.video_service import VideoEmbeddingStore

# ---------------------------
# Schemas
# ---------------------------


class FullTranscriptArgs(BaseModel):
    full_text_only: bool = Field(default=False)


class SearchVideoArgs(BaseModel):
    query: str = Field(description="User query for search.")


class NoArgs(BaseModel):
    pass


# ---------------------------
# Helpers
# ---------------------------
TIMESTAMP_RE = re.compile(r"(?:(\d+):)?([0-5]?\d):([0-5]?\d)|(\d+):([0-5]?\d)")


def parse_timestamp(q: str) -> Optional[int]:
    m = TIMESTAMP_RE.search(q or "")
    if not m:
        return None
    if m.group(1):
        h, mm, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return h * 3600 + mm * 60 + s
    mm, s = int(m.group(4)), int(m.group(5))
    return mm * 60 + s


def normalize_query(q: str) -> str:
    q2 = (q or "").strip().lower()
    vague = {
        "what is in this video", "what is in this video?",
        "video", "content", "summary", "explain video",
        "please summarize", "what does he say", "what is he saying",
        "describe video", "what's in this video"
    }
    return "summary of entire video content and main ideas" if q2 in vague else q


def safe_text(value: Any) -> str:
    """
    Normalize LLM outputs that may be str | list[str|dict] | dict into a clean string.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts: List[str] = []
        for item in value:
            if isinstance(item, str):
                parts.append(item.strip())
            elif isinstance(item, dict):
                t = item.get("text") or item.get("content")
                if isinstance(t, str):
                    parts.append(t.strip())
        return " ".join([p for p in parts if p]).strip()
    if isinstance(value, dict):
        t = value.get("text") or value.get("content")
        if isinstance(t, str):
            return t.strip()
        return str(value)
    return str(value)


def chroma_filter(**kwargs) -> Dict[str, Any]:
    """
    Build a valid Chroma 'where' filter using $and.
    Example: chroma_filter(youtube_id='abc', field='snippet', lang='en')
    For list values, uses $in.
    """
    conditions = []
    for key, value in kwargs.items():
        if value is None:
            continue
        if isinstance(value, list):
            conditions.append({key: {"$in": value}})
        else:
            conditions.append({key: {"$eq": value}})
    return {"$and": conditions} if conditions else {}

# ---------------------------
# AgentState with tool_used flag to avoid loops
# ---------------------------


class AgentState(TypedDict):
    messages: List[BaseMessage]
    tool_used: bool

# ---------------------------
# VideoAgentService (final)
# ---------------------------


class VideoAgentService:
    def __init__(self, temperature: float = 0.0, model_name: str = "gemini-2.0-flash"):
        if not os.getenv("GOOGLE_API_KEY"):
            raise RuntimeError("GOOGLE_API_KEY is missing")
        self.llm = ChatGoogleGenerativeAI(
            model=model_name, temperature=temperature, max_retries=2)

    def chat(self, question: str, youtube_id: str, chat_history: list) -> dict:
        """
        Drop-in multilingual RAG chat method.
        Signature preserved: chat(self, question, youtube_id, chat_history)
        Returns: {"answer": str, "source_documents": []}
        """
        store = VideoEmbeddingStore()

        # --- detect user language ---
        try:
            user_lang = detect(question or "")
        except Exception:
            user_lang = "en"

        # --- collect available transcript languages from Chroma metadata ---
        def get_available_langs() -> List[str]:
            try:
                res = store.vs.get(
                    where={"youtube_id": youtube_id}, include=["metadatas"])
                langs = {md.get("lang") for md in res.get(
                    "metadatas", []) if md.get("lang")}
                return list(langs)
            except Exception:
                return []

        available_langs = get_available_langs()

        # choose RAG language: prefer user_lang, then English, then any
        if user_lang in available_langs:
            rag_lang = user_lang
        elif "en" in available_langs:
            rag_lang = "en"
        else:
            rag_lang = available_langs[0] if available_langs else "en"

        # --- rewrite user query into RAG language for retrieval only ---
        rewrite_prompt = (
            f"Rewrite the following question into language '{rag_lang}' ONLY for searching transcript text. "
            "Do NOT change names or timestamps, and do NOT add extra details. Return only the rewritten short query.\n\n"
            f"Question: {question}"
        )
        raw_rewrite = self.llm.invoke(rewrite_prompt).content
        rewritten_query = safe_text(raw_rewrite) or safe_text(question) or ""

        # --- prepare retrievers with valid Chroma filters ---
        transcript_where = chroma_filter(
            youtube_id=youtube_id, field="snippet", lang=rag_lang)
        metadata_where = chroma_filter(youtube_id=youtube_id, field=[
                                       "title", "description", "uploader"])

        transcript_retriever = store.vs.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 8, "filter": transcript_where}
        )
        metadata_retriever = store.vs.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5, "filter": metadata_where}
        )

        # ---------------------------
        # Tools: transcript, full transcript, metadata
        # ---------------------------

        def search_impl(query: str) -> str:
            """Search transcript segments in selected language and return matched snippets with timestamps."""
            q_for_search = normalize_query(safe_text(rewritten_query))
            ts = parse_timestamp(query or "")
            try:
                docs = transcript_retriever.invoke(q_for_search)
            except Exception as e:
                # best-effort fallback: try without lang filter
                try:
                    fallback_where = chroma_filter(
                        youtube_id=youtube_id, field="snippet")
                    fallback_retriever = store.vs.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": 8, "filter": fallback_where}
                    )
                    docs = fallback_retriever.invoke(q_for_search)
                except Exception as e2:
                    return f"Error searching transcript: {str(e)} | fallback error: {str(e2)}"

            # narrow by timestamp window if requested
            if ts is not None and docs:
                try:
                    docs = [
                        d for d in docs
                        if d.metadata and d.metadata.get("start") is not None and abs(float(d.metadata.get("start", 0)) - float(ts)) <= 30
                    ] or docs
                except Exception:
                    pass

            if not docs:
                return "No transcript found in the selected language."

            out_parts: List[str] = []
            for d in docs:
                st = d.metadata.get("start", "?") if getattr(
                    d, "metadata", None) else "?"
                out_parts.append(f"[{st}s] {d.page_content}")
            return "\n\n".join(out_parts)

        transcript_tool = StructuredTool.from_function(
            name="search_video_transcript",
            func=search_impl,
            args_schema=SearchVideoArgs,
            description="Search transcript segments of the selected video and return matches with timestamps."
        )

        def full_impl(full_text_only: bool = False) -> str:
            """Return the full stored transcript (raw or as text)."""
            try:
                tx = store.get_transcript(youtube_id, full_text_only)
                if not tx:
                    return "Transcript unavailable."
                t = str(tx)
                return t[:100000] + "..." if len(t) > 100000 else t
            except Exception as e:
                return f"Error fetching transcript: {str(e)}"

        full_tool = StructuredTool.from_function(
            name="get_full_document_text",
            func=full_impl,
            args_schema=FullTranscriptArgs,
            description="Return the entire transcript for the video (raw or structured)."
        )

        def metadata_impl() -> str:
            """Return title/description/uploader stored in vector DB metadata (best-effort)."""
            try:
                docs = metadata_retriever.invoke("title description uploader")
            except Exception:
                # fallback to direct collection read
                try:
                    res = store.vs.get(where={"youtube_id": youtube_id}, include=[
                                       "metadatas", "documents"])
                    docs = []
                    for text, md in zip(res.get("documents", []), res.get("metadatas", [])):
                        if md.get("field") in ("title", "description", "uploader"):
                            class D:
                                page_content = text
                                metadata = md
                            docs.append(D())
                except Exception as e2:
                    return f"Metadata error: {str(e2)}"

            if not docs:
                return "No metadata found."
            uniq = {safe_text(getattr(d, "page_content", "")) for d in docs}
            return "\n".join([u for u in uniq if u])

        metadata_tool = StructuredTool.from_function(
            name="get_video_metadata",
            func=metadata_impl,
            args_schema=NoArgs,
            description="Fetch video metadata such as title, description, and uploader."
        )

        tools = [transcript_tool, full_tool, metadata_tool]
        llm_with_tools = self.llm.bind_tools(tools)

        # ---------------------------
        # LangGraph agent node & recursion protection
        # ---------------------------
        def agent_node(state: AgentState):
            raw_msgs: List[BaseMessage] = list(state["messages"])
            fixed_msgs: List[BaseMessage] = []

            # ensure at least one HumanMessage exists (Gemini requirement)
            if not any(isinstance(m, HumanMessage) for m in raw_msgs):
                raw_msgs.append(HumanMessage(content=safe_text(question)))

            # sanitize contents
            for m in raw_msgs:
                if isinstance(m, AIMessage) and not safe_text(getattr(m, "content", None)):
                    fixed_msgs.append(
                        AIMessage(content=" ", tool_calls=getattr(m, "tool_calls", None)))
                    continue
                if hasattr(m, "content"):
                    try:
                        m.content = safe_text(
                            getattr(m, "content", None)) or " "
                    except Exception:
                        pass
                fixed_msgs.append(m)

            # If tools already used this turn, avoid allowing LLM to request them again
            tools_used_before = state.get("tool_used", False)

            resp = llm_with_tools.invoke(fixed_msgs)
            resp.content = safe_text(getattr(resp, "content", None)) or " "

            # If LLM still wants to call tools but we've already used tools -> strip calls to stop loop
            if getattr(resp, "tool_calls", None) and tools_used_before:
                resp.tool_calls = []

            return {"messages": [resp]}

        # build graph
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_edge(START, "agent")

        def should_continue(state: AgentState) -> str:
            last = state["messages"][-1]
            # stop immediately if we already executed tools this invocation
            if state.get("tool_used", False):
                return END
            # if LLM wants tool -> mark tool_used and continue once
            if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
                state["tool_used"] = True
                return "tools"
            return END

        workflow.add_conditional_edges("agent", should_continue)
        workflow.add_edge("tools", "agent")
        app = workflow.compile()

        # ---------------------------
        # system prompt & build input state
        # ---------------------------
        system_prompt = f"""
You are a multilingual video assistant.
USER LANGUAGE: {user_lang}
TRANSCRIPT LANGUAGE USED FOR RAG: {rag_lang}

RULES:
1. Answer in the user's language ({user_lang}).
2. Do not ask the user for more input.
3. Use 'search_video_transcript' for transcript lookups and 'get_video_metadata' only for metadata.
4. Use only tool outputs for factual assertions. Do not hallucinate.
"""

        input_messages: List[BaseMessage] = [
            SystemMessage(content=system_prompt)]
        for m in chat_history:
            input_messages.append(m if isinstance(
                m, BaseMessage) else HumanMessage(content=safe_text(m)))
        input_messages.append(HumanMessage(content=safe_text(question)))

        state: AgentState = {"messages": list(
            input_messages), "tool_used": False}

        # invoke graph (recursion_limit can be tuned)
        result = app.invoke(state, config={"recursion_limit": 10})

        final_text = ""
        if result and result.get("messages"):
            final_text = safe_text(result["messages"][-1].content)

        return {"answer": final_text, "source_documents": []}
