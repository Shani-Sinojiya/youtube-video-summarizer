# """
# VideoRAGService for YouTube Summarizer.
# Modern implementation using create_history_aware_retriever + create_retrieval_chain.
# """

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables import Runnable
# from langchain_core.vectorstores import VectorStoreRetriever
# from langchain_core.messages import BaseMessage

# class RAGService:
#     def __init__(self, temperature: float = 0.7, model_name: str = "gemini-2.5-flash"):
#         """
#         Initialize the RAG Service with Google Gemini.
        
#         Args:
#             temperature: Creativity of the model (0.0 to 1.0).
#             model_name: "gemini-1.5-flash" is recommended for speed/cost. 
#                         Use "gemini-1.5-pro" for complex reasoning.
#         """
#         self.llm = ChatGoogleGenerativeAI(
#             model=model_name,
#             temperature=temperature,
#             max_tokens=None,
#             timeout=None,
#             max_retries=2,
#         )

#         # --- Prompt 1: Contextualize Question ---
#         # This prompt takes the chat history and the new question, and rephrases the 
#         # question to be standalone so the vector search understands it.
#         self.contextualize_q_system_prompt = (
#             "Given a chat history and the latest user question "
#             "which might reference context in the chat history, "
#             "formulate a standalone question which can be understood "
#             "without the chat history. Do NOT answer the question, "
#             "just reformulate it if needed and otherwise return it as is."
#         )

#         self.contextualize_q_prompt = ChatPromptTemplate.from_messages([
#             ("system", self.contextualize_q_system_prompt),
#             MessagesPlaceholder("chat_history"),
#             ("human", "{input}"),
#         ])
        
#         # --- Prompt 2: Answer Question ---
#         # This prompt takes the chat history and the new question, and rephrases the 
#         # question to be standalone so the vector search understands it.
#         self.qa_system_prompt = (
#             "You are a helpful AI assistant for a YouTube video analysis tool. "
#             "Use the following pieces of retrieved context to answer "
#             "the question. \n\n"
#             "Rules:\n"
#             "1. Answer strictly based on the provided context.\n"
#             "2. If the answer is not in the context, say 'I cannot find that information in this video.'\n"
#             "3. Keep the answer concise and friendly.\n\n"
#             "Context:\n{context}"
#         )

#         self.qa_prompt = ChatPromptTemplate.from_messages([
#             ("system", self.qa_system_prompt),
#             MessagesPlaceholder("chat_history"),
#             ("human", "{input}"),
#         ])

#     def get_rag_chain(self, retriever: VectorStoreRetriever) -> Runnable:
#         """
#         Constructs the LCEL RAG chain dynamically based on the provided retriever.
#         """
        
#         # 1. History Aware Retriever Chain
#         # (Input + History) -> Rewritten Question -> Vector Store -> Documents
#         history_aware_retriever = create_history_aware_retriever(
#             self.llm,
#             retriever,
#             self.contextualize_q_prompt
#         )

#         # 2. Document Processing Chain
#         # (Documents + Question) -> LLM -> Answer
#         question_answer_chain = create_stuff_documents_chain(
#             self.llm,
#             self.qa_prompt
#         )

#         # 3. Final RAG Chain
#         # Connects the two previous chains
#         rag_chain = create_retrieval_chain(
#             history_aware_retriever, 
#             question_answer_chain
#         )

#         return rag_chain

#     def build_chain(self, retriever, chat_history):
#         """Build a modern conversational RAG chain."""
#         # History-aware retriever
#         history_aware_retriever = create_history_aware_retriever(
#             self.llm,
#             retriever,
#             self.contextualize_q_prompt,
#         )

#         # QA chain
#         qa_chain = create_stuff_documents_chain(
#             self.llm,
#             self.qa_prompt,
#         )

#         # Final retrieval chain
#         rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

#         return rag_chain

#     def chat(self, question: str, vectorstore, chat_history):
#         """Run a chat query against the modern RAG chain."""
#         chain = self.build_chain(vectorstore, chat_history)

#         # Get messages from history object
#         messages = chat_history.messages if hasattr(chat_history, 'messages') else []

#         # Invoke chain with both question and chat history
#         result = chain.invoke({
#             "input": question,
#             "chat_history": messages
#         })

#         return result
