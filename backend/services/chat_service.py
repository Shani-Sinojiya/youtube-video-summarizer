

import os
from langchain_mongodb import MongoDBChatMessageHistory

from services.rag_service import RAGService
from services.video_service import VideoEmbeddingStore


class ChatHistory:
    def __init__(self, chat_id: str) -> None:
        self.chat_id = chat_id
        self.history = []

        self.chat_message_history = MongoDBChatMessageHistory(
            session_id=self.chat_id,
            connection_string=os.getenv("MONGODB_URI"),
            database_name=os.getenv("DATABASE_NAME", "yt_summarizer"),
            collection_name="chat_histories",
        )

    async def add_user_message(self, message: str) -> None:
        self.chat_message_history.add_user_message(message)
        self.history.append({"role": "user", "content": message})

    async def add_ai_message(self, message: str) -> None:
        self.chat_message_history.add_ai_message(message)
        self.history.append({"role": "ai", "content": message})

    async def get_history(self) -> list:
        history = self.chat_message_history.messages
        return history


class Chat_Service(ChatHistory):
    def __init__(self, video_id: str, db, chat_id: str):
        super().__init__(chat_id)
        self.video_id = video_id
        self.db = db
        self.chat_id = chat_id

    async def get_video(self):
        video = await self.db.videos.find_one({"youtube_id": self.video_id})
        return video

    async def answer_question(self, question: str) -> str:
        video = await self.get_video()

        if not video:
            return "Video not found."

        if video.get("status") != "completed":
            return "Video processing not completed."

        model = RAGService(temperature=0.7)
        embedding_store = VideoEmbeddingStore()

        # Get the vectorstore instance and configure it with the specific video filter
        vs = embedding_store.vs.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5, "filter": {"youtube_id": self.video_id}}
        )

        # Use the configured retriever in the chat
        result = model.chat(question, vs, self.chat_message_history)

        # Add the current question to history before getting answer
        await self.add_user_message(question)

        # Extract answer from result
        answer = result.get(
            "answer", "I'm sorry, I don't have an answer for that.")

        # Add the answer to chat history
        await self.add_ai_message(answer)

        return answer
