"""
Service for processing YouTube videos in the background.
Handles video information extraction, transcript fetching, and vector storage.
"""

from typing import Any, Optional, Dict, List
from datetime import datetime
from bson import ObjectId
from langchain_chroma import Chroma
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.video import Video
from utils.youtube_info_extractor import YouTubeInfoExtractor
from utils.youtube_transcribe import YouTubeTranscriber

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document


class VideoEmbeddingStore:
    """Vector store for video embeddings."""

    def __init__(self):
        # Embedding model (Gemini)
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        self.vs = Chroma(
            collection_name="example_collection",
            embedding_function=self.embedding_model,
            persist_directory="./chroma_langchain_db")

    # ---------- Writer ----------

    def add_video_embeddings(
        self,
        youtube_id: str,
        title: str,
        description: str,
        uploader: str,
        snippets: List[Dict[str, Any]],
        language: str = "en"
    ):
        docs: List[Document] = []
        base_meta = {"youtube_id": youtube_id, "lang": language}

        if title:
            docs.append(Document(page_content=title, metadata={
                        **base_meta, "field": "title"}))
        if description:
            docs.append(Document(page_content=description, metadata={
                        **base_meta, "field": "description"}))
        if uploader:
            docs.append(Document(page_content=f"Uploaded by {uploader}", metadata={
                        **base_meta, "field": "uploader"}))

        for s in snippets:
            text = s.get("text")
            if text:
                md = {**base_meta, "field": "snippet",
                      "start": s.get("start"), "duration": s.get("duration")}
                docs.append(Document(page_content=text, metadata=md))

        self.vs.add_documents(docs)
        return f"✅ Stored {len(docs)} embeddings for video {youtube_id}"

    # ---------- Reader ----------
    def search_video(self, youtube_id: str, query: str, k: int = 5):
        retriever = self.vs.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k, "filter": {"youtube_id": youtube_id}}
        )
        return retriever.get_relevant_documents(query)


class VideoService:
    """Service for processing a YouTube video and storing embeddings."""

    def __init__(self, video_id: str, db: AsyncIOMotorDatabase):
        self.video_id = video_id
        self.db = db
        self.db_videos = db.videos
        self.info_extractor = YouTubeInfoExtractor()
        self.transcriber: Optional[YouTubeTranscriber] = None
        self.embedding_store = VideoEmbeddingStore()

    async def initialize(self):
        await self.update_video_status("processing")

    async def save_video_info(self, video_info: Video) -> None:
        await self.db_videos.insert_one(video_info.dict())

    async def update_video_info(self, video_info: Video) -> None:
        await self.db_videos.update_one(
            {"_id": ObjectId(self.video_id)},
            {"$set": video_info.dict(exclude_unset=True)}
        )

    async def update_video_status(self, status: str, error: Optional[str] = None) -> None:
        update_data = {"status": status, "updated_at": datetime.utcnow()}
        if error:
            update_data["processing_error"] = error
            update_data["processed_at"] = datetime.utcnow()
        await self.db_videos.update_one(
            {"_id": ObjectId(self.video_id)},
            {"$set": update_data}
        )

    async def fetch_video_info(self) -> Optional[Video]:
        video = await self.db_videos.find_one({"_id": ObjectId(self.video_id)})
        return Video(**video) if video else None

    async def process_video(self) -> None:
        """Process video metadata, transcripts, and store embeddings."""
        try:
            video = await self.fetch_video_info()
            if not video:
                raise ValueError(
                    f"Video {self.video_id} not found in database")

            # Initialize transcriber
            self.transcriber = YouTubeTranscriber(video.youtube_id)

            # Fetch YouTube info
            url = f"https://www.youtube.com/watch?v={video.youtube_id}"
            try:
                info = self.info_extractor.get_info(url)
                video.title = str(info["title"])
                video.thumbnail_url = str(info["thumbnail"])
                video.description = str(info["description"])
                video.duration_seconds = int(info.get("duration_seconds") or 0)
                video.view_count = int(info.get("views") or 0)
                video.uploader = str(info["uploader"])
                video.channel_url = str(info["channel_url"])
                video.updated_at = datetime.utcnow()
                await self.update_video_info(video)
            except Exception as e:
                raise ValueError(f"Failed to extract video info: {str(e)}")

            # Fetch transcripts
            transcripts = self.transcriber.get_all_transcripts()
            if not transcripts:
                raise ValueError("No transcripts available for this video")

            video.available_languages = list(transcripts.keys())
            video.default_language = "en" if "en" in transcripts else video.available_languages[
                0]
            video.transcripts = transcripts
            video.status = "processing"
            video.processing_error = None
            video.processed_at = datetime.utcnow()
            await self.update_video_info(video)

            # -------- Store embeddings for all languages --------
            for lang, data in transcripts.items():
                snippets = []
                if isinstance(data, dict) and "snippets" in data:
                    snippets = data["snippets"]  # type: ignore
                elif isinstance(data, list):
                    snippets = data
                self.embedding_store.add_video_embeddings(
                    youtube_id=video.youtube_id,
                    title=video.title,
                    description=video.description,
                    uploader=video.uploader,
                    snippets=snippets,
                    language=lang
                )

            # Mark as completed
            await self.update_video_status("completed")

        except Exception as e:
            await self.update_video_status("failed", str(e))
            raise

    async def fetch_video_info_youtube(self) -> Dict[str, Optional[str]] | None:
        """Fetch video details using YouTubeInfoExtractor."""
        extractor = YouTubeInfoExtractor()
        return extractor.get_info(f"https://www.youtube.com/watch?v={self.video_id}")
