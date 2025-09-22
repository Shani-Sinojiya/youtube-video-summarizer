import asyncio
from services.video_service import VideoService
from db.mongodb import get_db

# Shared in-memory job queue
job_queue = asyncio.Queue()


async def worker(name: str, db=get_db):
    """Worker that takes jobs from queue and processes them."""
    while True:
        job = await job_queue.get()
        print(f"[{name}] Processing video {job}...")

        video_service = VideoService(video_id=job, db=db)
        try:
            # Initialize the service first
            await video_service.initialize()
            # Then process the video
            await video_service.process_video()
            print(f"[{name}] Successfully processed video {job}")
        except Exception as e:
            print(f"[{name}] Error processing video {job}: {e}")
            # Update video status to failed if there's an error
            await video_service.update_video_status("failed", str(e))

        print(f"[{name}] Finished video {job}")
        job_queue.task_done()


async def add_task(task: str):
    await job_queue.put(task)
    print(f"[Producer] Added video: {task}")
