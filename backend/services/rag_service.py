from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate

from services.video_service import VideoEmbeddingStore


class VideoRAGService:
    """
    High-quality RAG system for YouTube videos.
    Supports:
    - Accurate Q&A
    - Detailed fallback summarizer (full transcript)
    - Metadata-aware answers
    - Multilingual response
    """

    SUMMARY_KEYWORDS = [
        "summarize", "summary", "what inside",
        "explain the video", "explain video",
        "in detail", "detailed", "overview",
        "describe", "what happens", "what is inside"
    ]

    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        temperature: float = 0.2,
        k: int = 8,
    ):
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_retries=2,
        )

        self.store = VideoEmbeddingStore()
        self.vs = self.store.vs
        self.k = k

        self.prompt = PromptTemplate.from_template("""
You are a highly accurate assistant answering questions about a YouTube video.

Context may include:
- Transcript snippets
- Title & description
- Channel name
- Video duration
- Upload date
- Views
- Any metadata

RULES:
1. Answer ONLY using context.
2. If transcript does NOT contain the answer, check metadata.
3. If still missing, reply: "I could not find this information in the video."
4. Respond in the user's language.
5. Keep answers clear and human-friendly.

User question:
{input}

Context:
{context}

Answer:
""")

    # -------------------------------------------------------------
    # Detect if user wants a full summary instead of vector search
    # -------------------------------------------------------------
    def is_summary_question(self, q: str) -> bool:
        q = q.lower()
        return any(key in q for key in self.SUMMARY_KEYWORDS)

    # -------------------------------------------------------------
    # Fallback full transcript summarizer
    # -------------------------------------------------------------
    def summarize_full_transcript(self, youtube_id: str, question: str) -> str:
        transcript = self.store.get_transcript(youtube_id, full_text_only=True)

        if not transcript or len(transcript.strip()) < 10:
            return "I could not find transcript content for this video."

        prompt = f"""
You are a deep video summarizer.

User request:
{question}

Task:
Provide an extremely detailed explanation of the ENTIRE video content.
Include:
- What the speaker explains
- Key points
- Step-by-step concepts
- Examples
- Purpose of the video
- Intended audience
- Tone & style

Transcript:
{transcript}

Detailed summary:
"""

        resp = self.llm.invoke(prompt)
        return getattr(resp, "content", str(resp))

    # -------------------------------------------------------------
    # Build retriever for normal Q&A
    # -------------------------------------------------------------
    def get_retriever(self, youtube_id: str):
        return self.vs.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": self.k,
                "filter": {"youtube_id": {"$eq": youtube_id}},
            }
        )

    # -------------------------------------------------------------
    # MAIN PUBLIC METHOD
    # -------------------------------------------------------------
    def answer(self, youtube_id: str, question: str) -> Dict[str, Any]:

        # STEP 1 — If it's a summary question → bypass RAG, use full transcript
        if self.is_summary_question(question):
            answer = self.summarize_full_transcript(youtube_id, question)
            return {"answer": answer, "docs": []}

        # STEP 2 — Normal RAG flow
        retriever = self.get_retriever(youtube_id)

        combine_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=self.prompt,
        )

        rag_chain = create_retrieval_chain(retriever, combine_chain)

        try:
            result = rag_chain.invoke({"input": question})
        except Exception as e:
            return {"answer": f"RAG Error: {str(e)}", "docs": []}

        raw_answer = result.get("answer") or result.get("output") or ""

        # STEP 3 — If RAG failed to find context → fallback to transcript summary
        if "not mentioned" in raw_answer.lower() or raw_answer.strip() == "":
            fallback = self.summarize_full_transcript(youtube_id, question)
            return {"answer": fallback, "docs": []}

        return {
            "answer": raw_answer,
            "docs": result.get("context", []),
        }

    # -------------------------------------------------------------
    # Optional helper: Full transcript text
    # -------------------------------------------------------------
    def full_transcript(self, youtube_id: str) -> str:
        return self.store.get_transcript(youtube_id, full_text_only=True) or ""
