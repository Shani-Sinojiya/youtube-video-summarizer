from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


class UserProfile(BaseModel):
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    website: Optional[str]
    social_links: Optional[Dict[str, str]]  # Platform -> URL
    timezone: Optional[str]
    notification_settings: Optional[Dict[str, bool]]


class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    password_hash: str
    preferred_language: str = "en"  # Default to English
    preferred_model: str = "gemini-2.5-flash"  # Default Gemini model
    profile: Optional[UserProfile]
    created_at: Optional[datetime]
    last_login: Optional[datetime]
    active_chats: Optional[List[str]]  # List of active chat IDs
    total_videos: Optional[int] = 0
    storage_used: Optional[int] = 0  # in bytes
    account_type: str = "free"  # free, premium, etc.
    is_verified: bool = False
