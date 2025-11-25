"""
Retry queue service for managing failed video processing retries.
Handles scheduling, querying, and tracking retry attempts.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from models.video import Video


class RetryService:
    """Service for managing video processing retry queue."""

    def __init__(self, db: AsyncIOMotorDatabase, retry_interval_minutes: int = 10):
        """
        Initialize retry service.
        
        Args:
            db: MongoDB database instance
            retry_interval_minutes: Minutes to wait between retry attempts (default: 10)
        """
        self.db = db
        self.retry_interval_minutes = retry_interval_minutes
        self.videos_collection = db.videos

    async def get_videos_ready_for_retry(self) -> List[Video]:
        """
        Query videos that are ready to be retried.
        
        Returns videos with:
        - status = "failed"
        - retry_count < max_retries
        - next_retry_at <= current time (or None)
        """
        now = datetime.utcnow()
        
        query = {
            "status": "failed",
            "$expr": {"$lt": ["$retry_count", "$max_retries"]},
            "$or": [
                {"next_retry_at": {"$lte": now}},
                {"next_retry_at": None}
            ]
        }
        
        cursor = self.videos_collection.find(query)
        videos = []
        async for video_doc in cursor:
            try:
                # Ensure _id is converted to string
                if "_id" in video_doc:
                    video_doc["_id"] = str(video_doc["_id"])
                videos.append(Video(**video_doc))
            except Exception as e:
                print(f"Error parsing video {video_doc.get('_id')}: {e}")
        
        return videos

    async def schedule_retry(self, video_id: str) -> None:
        """
        Schedule a video for retry by calculating next retry time.
        
        Args:
            video_id: MongoDB ObjectId of the video
        """
        now = datetime.utcnow()
        next_retry = now + timedelta(minutes=self.retry_interval_minutes)
        
        await self.videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {
                "$set": {
                    "next_retry_at": next_retry,
                    "last_retry_at": now,
                    "updated_at": now
                },
                "$inc": {"retry_count": 1}
            }
        )

    async def should_retry(self, video_id: str) -> bool:
        """
        Check if a video is eligible for retry.
        
        Args:
            video_id: MongoDB ObjectId of the video
            
        Returns:
            True if video can be retried, False otherwise
        """
        video_doc = await self.videos_collection.find_one({"_id": ObjectId(video_id)})
        
        if not video_doc:
            return False
        
        retry_count = video_doc.get("retry_count", 0)
        max_retries = video_doc.get("max_retries", 5)
        status = video_doc.get("status")
        
        return status == "failed" and retry_count < max_retries

    async def reset_retry_state(self, video_id: str) -> None:
        """
        Reset retry state when video processing succeeds.
        
        Args:
            video_id: MongoDB ObjectId of the video
        """
        await self.videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {
                "$set": {
                    "retry_count": 0,
                    "last_retry_at": None,
                    "next_retry_at": None,
                    "updated_at": datetime.utcnow()
                }
            }
        )

    async def get_retry_statistics(self) -> dict:
        """
        Get statistics about retry queue.
        
        Returns:
            Dictionary with retry statistics
        """
        pipeline = [
            {
                "$match": {"status": "failed"}
            },
            {
                "$group": {
                    "_id": None,
                    "total_failed": {"$sum": 1},
                    "avg_retry_count": {"$avg": "$retry_count"},
                    "max_retry_count": {"$max": "$retry_count"},
                    "eligible_for_retry": {
                        "$sum": {
                            "$cond": [
                                {"$lt": ["$retry_count", "$max_retries"]},
                                1,
                                0
                            ]
                        }
                    }
                }
            }
        ]
        
        result = await self.videos_collection.aggregate(pipeline).to_list(length=1)
        
        if result:
            stats = result[0]
            stats.pop("_id", None)
            return stats
        
        return {
            "total_failed": 0,
            "avg_retry_count": 0,
            "max_retry_count": 0,
            "eligible_for_retry": 0
        }
