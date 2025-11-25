import os
from typing import TypedDict, List, Literal

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from services.video_service import VideoEmbeddingStore 

# --- 1. Schemas ---
class FullTranscriptArgs(BaseModel):
    full_text_only: bool = Field(default=False, description="If true, returns raw text without timestamps.")

class SearchVideoArgs(BaseModel):
    query: str = Field(description="The keyword or question to search for.")

class NoArgs(BaseModel):
    pass

class VideoAgentService:
    def __init__(self, temperature: float = 0.0, model_name: str = "gemini-2.0-flash"):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY environment variable is missing")

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_retries=2,
        )

    def chat(self, question: str, youtube_id: str, chat_history: list) -> dict:
        
        # 2. Setup Retriever
        store = VideoEmbeddingStore()
        retriever = store.get_retriever(youtube_id)

        # --- Tool 1: Search ---
        def search_impl(query: str) -> str:
            print(f"\n[🧠 AGENT SEARCH] Query: '{query}'")
            try:
                if not query or not query.strip():
                    query = "summary introduction main points"
                
                docs = retriever.invoke(query)
                if not docs:
                    return "No specific text found."
                
                results = []
                for d in docs:
                    field = d.metadata.get('field', 'snippet')
                    if field == 'snippet':
                        start = d.metadata.get('start', '?')
                        results.append(f"[Time: {start}s] {d.page_content}")
                    else:
                        results.append(f"[Metadata: {field}] {d.page_content}")
                return "\n\n".join(results)
            except Exception as e:
                return f"Error: {str(e)}"

        video_tool = StructuredTool.from_function(
            name="search_video_knowledge_base",
            func=search_impl,
            args_schema=SearchVideoArgs,
            description="Searches video content (transcript, title, metadata)."
        )

        # --- Tool 2: Full Text ---
        def get_full_transcript_impl(full_text_only: bool = False) -> str:
            print(f"\n[📜 AGENT FETCH] Full Transcript...")
            try:
                transcript = store.get_transcript(youtube_id, full_text_only=full_text_only)
                text_data = str(transcript)
                if len(text_data) > 100000:
                    return f"Transcript truncated (first 100k chars):\n{text_data[:100000]}..."
                return text_data
            except Exception as e:
                return f"Error: {str(e)}"

        full_transcript_tool = StructuredTool.from_function(
            name="get_full_document_text",
            func=get_full_transcript_impl,
            args_schema=FullTranscriptArgs,
            description="Retrieves full text. Use only if requested."
        )

        # --- Tool 3: Info ---
        def get_video_info_impl() -> str:
            print(f"\n[ℹ️ AGENT INFO] Fetching Metadata...")
            try:
                docs = retriever.invoke("Video Title Description Uploader")
                info = []
                for d in docs:
                    field = d.metadata.get('field', 'snippet')
                    if field in ['title', 'description', 'uploader']:
                        info.append(d.page_content)
                return "\n".join(list(set(info))) if info else "No metadata found."
            except Exception as e:
                return f"Error: {str(e)}"

        video_info_tool = StructuredTool.from_function(
            name="get_video_metadata",
            func=get_video_info_impl,
            args_schema=NoArgs,
            description="Retrieves video title, description, and uploader."
        )

        tools = [video_tool, full_transcript_tool, video_info_tool]
        llm_with_tools = self.llm.bind_tools(tools)

        # --- 3. Graph ---
        class AgentState(TypedDict):
            messages: List[BaseMessage]

        # ---------------------------------------------------------
        # 🛡️ THE FIX: RECREATE MESSAGES TO FORCE CONTENT 🛡️
        # ---------------------------------------------------------
        def agent_node(state: AgentState):
            raw_messages = state["messages"]
            final_messages = []
            
            for m in raw_messages:
                # If it is an AI Message with missing content (common in Tool Calls)
                if isinstance(m, AIMessage) and not m.content:
                    # Create a NEW OBJECT with a space character
                    # This ensures Pydantic/Immutable constraints don't block the fix
                    new_m = AIMessage(
                        content=" ", 
                        tool_calls=m.tool_calls,
                        additional_kwargs=m.additional_kwargs,
                        id=m.id
                    )
                    final_messages.append(new_m)
                else:
                    final_messages.append(m)
            
            # Invoke LLM with the CLEAN list
            response = llm_with_tools.invoke(final_messages)
            
            # Ensure the NEW response has content
            if not response.content:
                response.content = " "
                
            return {"messages": [response]}
        # ---------------------------------------------------------

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_edge(START, "agent")

        def should_continue(state: AgentState) -> Literal["tools", END]:
            last_message = state["messages"][-1]
            if last_message.tool_calls:
                return "tools"
            return END

        workflow.add_conditional_edges("agent", should_continue)
        workflow.add_edge("tools", "agent")

        app = workflow.compile()

        # --- 4. Prompt ---
        system_prompt = (
            "You are an expert AI Video Assistant.\n"
            "RULES:\n"
            "1. **SEARCH**: Use 'search_video_knowledge_base' for content questions.\n"
            "2. **INFO**: Use 'get_video_metadata' for Title/Description.\n"
            "3. **PROACTIVE**: If the user asks 'Summarize', search immediately.\n"
            "4. **NO APOLOGIES**: Just use the tools.\n"
            "5. **LANGUAGE**: Answer in the user's language."
        )

        input_messages = [SystemMessage(content=system_prompt)] + list(chat_history) + [HumanMessage(content=str(question))]
        
        result = app.invoke({"messages": input_messages}, config={"recursion_limit": 10})
        
        return {
            "answer": result["messages"][-1].content,
            "source_documents": [] 
        }