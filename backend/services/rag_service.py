"""
VideoRAGService for YouTube Summarizer.
Modern implementation using create_history_aware_retriever + create_retrieval_chain.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


class RAGService:
    def __init__(self, temperature: float = 0.7):
        """Initialize Gemini Flash 2.0 LLM."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=temperature,
        )

        # Prompt for contextualizing user questions using chat history
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Reformulate the user's question if needed to be more clear."),
            ("human", "{input}"),
        ])

        # Prompt for answering from retrieved context
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a YouTube video assistant. Use the context to answer questions clearly. Consider the chat history for context."),
            ("human", "Chat History:\n{chat_history}\n\nQuestion: {input}"),
            ("system", "Context from video:\n{context}"),
        ])

    def build_chain(self, retriever, chat_history):
        """Build a modern conversational RAG chain."""
        # History-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            self.llm,
            retriever,
            self.contextualize_q_prompt,
        )

        # QA chain with chat history included in the prompt
        qa_chain = create_stuff_documents_chain(
            self.llm,
            self.qa_prompt,
        )

        # Final retrieval chain
        rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

        return rag_chain

    def chat(self, question: str, vectorstore, chat_history):
        """Run a chat query against the modern RAG chain."""
        chain = self.build_chain(vectorstore, chat_history)

        # Format chat history as string
        history_str = "\n".join([
            f"{msg.type}: {msg.content}"
            for msg in chat_history.messages
        ]) if hasattr(chat_history, 'messages') else ""

        # Invoke chain with both question and chat history
        result = chain.invoke({
            "input": question,
            "chat_history": history_str
        })

        return result

        return {
            "answer": result.get("answer", ""),
            "context": result.get("context", []),  # optional debug
        }
