from pydantic import BaseModel
from typing import Optional, Dict, Literal
from datetime import datetime


class Video(BaseModel):
    id: Optional[str] = None
    _id: Optional[str] = None  # MongoDB document ID
    youtube_id: str
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None
    # Map of language_code -> transcript list
    transcripts: Dict[str, list[dict]] = {}
    default_language: str = "en"
    available_languages: list[str] = []
    status: Literal["pending", "processing", "completed", "failed"] = "pending"
    processing_error: Optional[str] = None
    # Map of language_code -> list of vector chunk IDs
    vector_ids: Optional[Dict[str, list[str]]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # When processing was completed or failed
    processed_at: Optional[datetime] = None
    description: Optional[str] = None  # Video description from YouTube
    duration_seconds: Optional[int] = None  # Video duration in seconds
    view_count: Optional[int] = None  # YouTube view count
    uploader: Optional[str] = None  # YouTube channel name
    channel_url: Optional[str] = None  # YouTube channel URL
    # Retry tracking fields
    retry_count: int = 0  # Number of retry attempts
    max_retries: int = 5  # Maximum allowed retries
    last_retry_at: Optional[datetime] = None  # Timestamp of last retry attempt
    next_retry_at: Optional[datetime] = None  # Scheduled time for next retry
    # Distributed locking fields
    processing_started_at: Optional[datetime] = None  # When processing started
    processing_worker_id: Optional[str] = None  # Which worker is processing
    lock_acquired_at: Optional[datetime] = None  # When lock was acquired
    processing_progress: Optional[str] = None  # Detailed progress status (e.g. "Vectorizing...")


class VideoUserUpload(BaseModel):
    id: Optional[str]
    user_id: str
    video_id: str
    uploaded_at: Optional[datetime]
