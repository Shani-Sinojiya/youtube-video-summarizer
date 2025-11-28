"""
Service for processing YouTube videos in the background.
Handles video information extraction, transcript fetching, and vector storage.
"""

from typing import Any, Optional, Dict, List
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_chroma import Chroma 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

from models.video import Video
from utils.youtube_info_extractor import YouTubeInfoExtractor
from utils.youtube_transcribe import YouTubeTranscriber
from services.retry_service import RetryService


class VideoEmbeddingStore:
    """Vector store for video embeddings."""

    def __init__(self):
        # Embedding model (Gemini)
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        self.vs = Chroma(
            collection_name="video_collection",
            embedding_function=self.embedding_model,
            persist_directory="./chroma_langchain_db")

    def add_video_embeddings(
        self,
        youtube_id: str,
        title: str,
        description: str,
        uploader: str,
        snippets: List[Dict[str, Any]],
        language: str = "en",
        duration_seconds: Optional[int] = None,
        channel_url: Optional[str] = None,
        view_count: Optional[int] = None,
        upload_date: Optional[datetime] = None,
        thumbnail_url: Optional[str] = None
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
            
        if duration_seconds is not None:
            docs.append(Document(page_content=f"Duration: {duration_seconds} seconds", metadata={
                        **base_meta, "field": "duration_seconds"}))
        if channel_url:
            docs.append(Document(page_content=channel_url, metadata={
                        **base_meta, "field": "channel_url"}))
        if view_count is not None:
            docs.append(Document(page_content=f"View count: {view_count}", metadata={
                        **base_meta, "field": "view_count"}))
        if upload_date:
            docs.append(Document(page_content=upload_date.isoformat(), metadata={
                        **base_meta, "field": "upload_date"}))
        if thumbnail_url:
            docs.append(Document(page_content=thumbnail_url, metadata={
                        **base_meta, "field": "thumbnail_url"}))

        for s in snippets:
            text = s.get("text")
            if text:
                # Ensure start is stored as a float/int for sorting later
                md = {
                    **base_meta, 
                    "field": "snippet",
                    "start": float(s.get("start", 0)), 
                    "duration": float(s.get("duration", 0))
                }
                docs.append(Document(page_content=text, metadata=md))

        self.vs.add_documents(docs)
        return f"✅ Stored {len(docs)} embeddings for video {youtube_id}"

    # ---------- New Method to Get Transcript ----------
    def get_transcript(self, youtube_id: str, full_text_only: bool = False) -> Any:
        """
        Retrieves the transcript snippets for a specific video using metadata filtering.
        It sorts them by timestamp to reconstruct the flow.
        """
        # 1. Direct fetch using metadata filter (No embedding cost involved)
        # We use $and to ensure we get specific video ID AND only transcript snippets (ignoring title/desc)
        results = self.vs.get(
            where={
                "$and": [
                    {"youtube_id": {"$eq": youtube_id}},
                    {"field": {"$eq": "snippet"}}
                ]
            },
            include=["metadatas", "documents"]
        )

        # 2. Reconstruct the data structure
        transcript_segments = []
        
        # Zip documents (text) and metadatas together
        if results['documents'] and results['metadatas']:
            for text, meta in zip(results['documents'], results['metadatas']):
                transcript_segments.append({
                    "text": text,
                    "start": meta.get("start", 0),
                    "duration": meta.get("duration", 0)
                })

        # 3. Sort by 'start' time to ensure chronological order
        # (Vector stores do not guarantee retrieval order)
        transcript_segments.sort(key=lambda x: x["start"])

        # 4. Return format
        if full_text_only:
            # Join all text with spaces
            return " ".join([seg["text"] for seg in transcript_segments])
        
        return transcript_segments

    def get_retriever(self, youtube_id: str, k: int = 10) -> VectorStoreRetriever:
        """
        Returns a retriever configured specifically for the given video ID.
        """
        return self.vs.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k, 
                "filter": {"youtube_id": youtube_id}
            }
        )

    def search_video(self, youtube_id: str, query: str, k: int = 5) -> List[Document]:
        """
        Performs a similarity search for a specific query.
        """
        retriever = self.get_retriever(youtube_id, k=k)
        # Updated: get_relevant_documents is deprecated, use invoke()
        return retriever.invoke(query)

class VideoService:
    """Service for processing a YouTube video and storing embeddings."""

    def __init__(self, video_id: str, db: AsyncIOMotorDatabase):
        self.video_id = video_id
        self.db = db
        self.db_videos = db.videos
        self.info_extractor = YouTubeInfoExtractor()
        self.transcriber: Optional[YouTubeTranscriber] = None
        self.embedding_store = VideoEmbeddingStore()
        self.retry_service = RetryService(db)


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
        
        # Schedule retry if failed and eligible
        if status == "failed":
            if await self.retry_service.should_retry(self.video_id):
                await self.retry_service.schedule_retry(self.video_id)
                print(f"[RetryService] Scheduled retry for video {self.video_id}")
            else:
                print(f"[RetryService] Video {self.video_id} exceeded max retries")
        elif status == "completed":
            # Reset retry state on success
            await self.retry_service.reset_retry_state(self.video_id)
            print(f"[RetryService] Reset retry state for video {self.video_id}")

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
            total_langs = len(transcripts)
            for idx, (lang, data) in enumerate(transcripts.items()):
                # Update progress
                progress_msg = f"Vectorizing language {lang} ({idx+1}/{total_langs})"
                await self.db_videos.update_one(
                    {"_id": ObjectId(self.video_id)},
                    {"$set": {
                        "processing_progress": progress_msg, 
                        "updated_at": datetime.utcnow()
                    }}
                )
                
                snippets = []
                if isinstance(data, dict) and "snippets" in data:
                    snippets = data["snippets"]  # type: ignore
                elif isinstance(data, list):
                    snippets = data
                self.embedding_store.add_video_embeddings(
                    youtube_id=video.youtube_id,
                    title=video.title,
                    duration_seconds=video.duration_seconds,
                    description=video.description,
                    uploader=video.uploader,
                    channel_url=video.channel_url,
                    view_count=video.view_count,
                    thumbnail_url=video.thumbnail_url,
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
