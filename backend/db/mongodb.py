"""
MongoDB database connection and configuration.
"""

import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.database import Database


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    def get_database_name(cls) -> str:
        """Get MongoDB database name from environment."""
        return os.getenv("DATABASE_NAME", "yt_summarizer")

    @classmethod
    def get_database_url(cls) -> str:
        """Get MongoDB connection URL from environment."""
        return os.getenv("MONGODB_URL", "mongodb://localhost:27017")

    @classmethod
    async def connect(cls):
        """Connect to MongoDB database."""
        if cls.client is None:
            # Initialize the client
            cls.client = AsyncIOMotorClient(cls.get_database_url())

            # Get the specific database
            db_name = cls.get_database_name()
            cls.db = cls.client[db_name]

            # Create indexes
            await cls.create_indexes()

    @classmethod
    async def close(cls):
        """Close MongoDB connection."""
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            cls.db = None

    @classmethod
    async def create_indexes(cls):
        """Create database indexes."""
        if cls.db is not None:
            # User indexes
            await cls.db.users.create_index("email", unique=True)

            # Video indexes
            await cls.db.videos.create_index("youtube_id")

            # User-Video relationship
            await cls.db.video_user_uploads.create_index(
                [("user_id", 1), ("video_id", 1)], unique=True
            )

            # Chat user indexes
            await cls.db.chat_users.create_index(
                [("chat_id", 1), ("user_id", 1), ("video_id", 1)], unique=True
            )

            await cls.db.chat_users.find({"user_id": "afdad"}).sort("created_at", -1).to_list(length=100)


async def get_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency for database access."""
    if MongoDB.db is None:
        await MongoDB.connect()
    if MongoDB.db is None:
        raise RuntimeError("Database connection not established")
    return MongoDB.db
