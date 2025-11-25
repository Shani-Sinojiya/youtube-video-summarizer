from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel,  HttpUrl
from models.user import User
from db.mongodb import get_db
from datetime import datetime
from services.auth_service import get_current_user
from utils.youtube_url_parser import YouTubeParser
from models.video import Video
from worker.main import add_task


class VideoUploadRequest(BaseModel):
    url: HttpUrl


router = APIRouter(prefix="/video", tags=["video"])


@router.post("/upload", response_model=dict)
async def upload_video(
    request: VideoUploadRequest,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Endpoint to upload a YouTube video by URL.
    """
    youtube_id = YouTubeParser(str(request.url)).video_id
    if not youtube_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    # Check if video already exists
    existing_video = await db.videos.find_one({"youtube_id": youtube_id})

    if existing_video:
        # Check if this user already uploaded it
        is_exist_in_user = await db.video_user_uploads.find_one({
            "user_id": str(current_user.id),
            "video_id": str(existing_video["_id"]),
        })
        if is_exist_in_user:
            raise HTTPException(
                status_code=400, detail="Video already uploaded"
            )
        # If video exists but not linked to this user → link it
        await db.video_user_uploads.insert_one({
            "user_id": str(current_user.id),
            "video_id": str(existing_video["_id"]),
            "uploaded_at": datetime.utcnow(),
        })
        return {"message": "Video linked to user", "video_id": str(existing_video["_id"])}

    # Create a new video
    now = datetime.utcnow()
    video = Video(
        youtube_id=youtube_id,
        status="pending",
        created_at=now,
        updated_at=now,
    )
    video_data = video.model_dump(exclude_none=True)

    result = await db.videos.insert_one(video_data)
    video_id = str(result.inserted_id)

    # Link video to user
    await db.video_user_uploads.insert_one({
        "user_id": str(current_user.id),
        "video_id": video_id,
        "uploaded_at": datetime.utcnow(),
    })

    # Trigger async processing
    added = await add_task(video_id)
    if not added:
        print(f"Video {video_id} already in processing queue")

    return {"message": "Video upload initiated", "video_id": video_id}


@router.get("/{video_id}", response_model=Video)
async def get_video(video_id: str, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """
    Endpoint to get video information by video ID.
    """
    video = await db.videos.find_one({"youtube_id": video_id})
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Access the transcripts
    if "transcripts" in video:
        # Extract snippets from transcript objects
        for lang, transcript in video["transcripts"].items():
            if isinstance(transcript, dict) and "snippets" in transcript:
                video["transcripts"][lang] = transcript["snippets"]

    return Video(**video)


@router.get("/", response_model=list[Video])
async def list_videos(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """
    Endpoint to list all videos uploaded by the current user.
    """
    user_videos_cursor = db.video_user_uploads.find(
        {"user_id": str(current_user.id)})
    user_video_ids = [ObjectId(entry["video_id"]) async for entry in user_videos_cursor]

    videos_cursor = db.videos.find({"_id": {"$in": user_video_ids}}, projection={
                                   "transcripts": 0, "vector_ids": 0})
    videos = [Video(**video) async for video in videos_cursor]

    return videos
