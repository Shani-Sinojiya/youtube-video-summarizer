from pydantic import BaseModel
from datetime import datetime


class ChatUser(BaseModel):
    id: str
    user_id: str
    chat_id: str
    video_id: str
    created_at: datetime
