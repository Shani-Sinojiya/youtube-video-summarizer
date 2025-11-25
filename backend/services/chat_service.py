import os
import traceback
from typing import List, Dict, Any
from fastapi import HTTPException
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.messages import BaseMessage
from services.video_service import VideoEmbeddingStore
from services.video_agent_service import VideoAgentService

# --- 1. Chat History Class (Standalone) ---
class ChatHistory:
    def __init__(self, chat_id: str) -> None:
        self.chat_id = chat_id
        
        # Initialize the LangChain MongoDB History
        self.chat_message_history = MongoDBChatMessageHistory(
            session_id=self.chat_id,
            connection_string=os.getenv("MONGODB_URI"),
            database_name=os.getenv("DATABASE_NAME", "yt_summarizer"),
            collection_name="chat_histories",
        )

    @property
    def messages(self) -> List[BaseMessage]:
        """Property to access messages directly."""
        return self.chat_message_history.messages

    async def add_user_message(self, message: str) -> None:
        """Adds a user message."""
        self.chat_message_history.add_user_message(message)

    async def add_ai_message(self, message: str) -> None:
        """Adds an AI message."""
        self.chat_message_history.add_ai_message(message)

    async def clear_history(self) -> None:
        """Clears the chat history."""
        self.chat_message_history.clear()


# --- 2. Chat Service Class (Uses ChatHistory via Composition) ---
class Chat_Service:  # <--- CHANGED: Removed (ChatHistory) inheritance
    def __init__(self, video_id: str, db, chat_id: str):
        self.video_id = video_id
        self.db = db
        self.chat_id = chat_id

        # Composition: We own an instance of ChatHistory
        self.history_manager = ChatHistory(chat_id)
        
        self.embedding_store = VideoEmbeddingStore()
        
        # CHANGED: Lowered temperature to 0.2. 
        # Agents need low temp to reliably call tools; 0.7 makes them hallucinate.
        self.agent_service = VideoAgentService(temperature=0.2)

    async def get_history(self) -> List[Dict[str, str]]:
        """Retrieves history for the API (JSON format)."""
        raw_messages = self.history_manager.messages
        formatted_history = []
        
        for msg in raw_messages:
            role = "user" if msg.type == "human" else "ai"
            if msg.content:
                formatted_history.append({
                    "role": role, 
                    "content": msg.content
                })
            
        return formatted_history

    async def get_video(self):
        return await self.db.videos.find_one({"youtube_id": self.video_id})

    async def answer_question(self, question: str) -> str:
        # 1. Validation
        if not question or not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        video = await self.get_video()
        if not video or video.get("status") != "completed":
            raise HTTPException(status_code=400, detail="Video processing not completed")

        # HISTORY SANITIZATION
        raw_history = self.history_manager.messages
        clean_history = []
        
        for msg in raw_history:
            # Force empty content to be a SPACE
            if not msg.content:
                msg.content = " "
            
            # Basic validity check
            has_content = len(str(msg.content).strip()) > 0
            has_tools = hasattr(msg, 'tool_calls') and len(msg.tool_calls) > 0
            
            if has_content or has_tools:
                clean_history.append(msg)

        # Run Agent
        try:
            result = self.agent_service.chat(
                question=question,
                youtube_id=self.video_id, 
                chat_history=clean_history
            )
            answer_text = result["answer"]
        except ValueError:
            # Retry fresh
            result = self.agent_service.chat(
                question=question,
                youtube_id=self.video_id,
                chat_history=[] 
            )
            answer_text = result["answer"]
        except Exception as e:
            print(f"Error: {e}")
            answer_text = "Error processing request."

        # Save
        if answer_text:
            await self.history_manager.add_user_message(question)
            await self.history_manager.add_ai_message(answer_text)

        return answer_text