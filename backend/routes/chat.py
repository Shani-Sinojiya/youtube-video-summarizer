from datetime import datetime
from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.user import User
from db.mongodb import get_db
from services.auth_service import get_current_user
import uuid


class ChatRequest(BaseModel):
    video_id: str
    question: str
    temperature: float = 0.7
    is_new_chat: bool = False
    chat_id: Optional[str] = None


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=dict)
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """
    Endpoint to ask questions about a processed video.
    """
    video = await db.videos.find_one({"youtube_id": request.video_id})
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if video.get("status") != "completed":
        raise HTTPException(
            status_code=400, detail="Video processing not completed")

    if not request.chat_id:
        if request.is_new_chat:
            # Optionally, clear previous chat history if needed
            request.chat_id = str(uuid.uuid4())
        elif not request.chat_id:
            raise HTTPException(
                status_code=400, detail="chat_id must be provided for existing chats")

    from services.chat_service import Chat_Service
    chat_service = Chat_Service(
        video_id=request.video_id, db=db, chat_id=request.chat_id)

    answer = await chat_service.answer_question(request.question)

    await db.chat_users.update_one(
        {"chat_id": request.chat_id, "user_id": current_user.id,
            "video_id": request.video_id},
        {"$setOnInsert": {
            "chat_id": request.chat_id,
            "user_id": current_user.id,
            "video_id": request.video_id,
            "created_at": datetime.utcnow()
        }},
        upsert=True
    )

    return {"answer": answer}


@router.get("/history/{chat_id}", response_model=dict)
async def get_chat_history(chat_id: str, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """
    Endpoint to retrieve chat history by chat_id.
    """
    from services.chat_service import ChatHistory
    chat_service = ChatHistory(chat_id=chat_id)

    history = await chat_service.get_history()
    if not history:
        print(f"Chat history for {history} not found")
        raise HTTPException(status_code=404, detail="Chat history not found")

    return {"chat_id": chat_id, "history": history}


@router.get("/history", response_model=dict)
async def list_chat_histories(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """
    Endpoint to list all chat histories for the current user.
    """

    data = await db.chat_users.find({"user_id": current_user.id}).sort("created_at", -1).to_list(length=100)
    if not data:
        raise HTTPException(status_code=404, detail="No chat histories found")

    chats = [{"chat_id": chat["chat_id"], "video_id": chat["video_id"],
              "created_at": chat["created_at"]} for chat in data]

    return {"chat_histories": chats}
