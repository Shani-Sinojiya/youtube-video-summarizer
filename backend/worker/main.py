"""
Smart async worker pool with duplicate prevention and distributed locking.
Manages multiple workers processing video tasks concurrently.
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Set
from bson import ObjectId
from services.video_service import VideoService
from services.retry_service import RetryService

# Shared in-memory job queue
job_queue = asyncio.Queue()

# Track queued and processing tasks to prevent duplicates
active_tasks: Set[str] = set()
task_lock = asyncio.Lock()


class WorkerPool:
    """Manages a pool of async workers for video processing."""

    def __init__(self, db, num_workers: int = 3, lock_timeout_minutes: int = 5):
        """
        Initialize worker pool.
        
        Args:
            db: MongoDB database instance
            num_workers: Number of concurrent workers (default: 3)
            lock_timeout_minutes: Minutes before auto-releasing stuck tasks (default: 5)
        """
        self.db = db
        self.num_workers = num_workers
        self.lock_timeout_minutes = lock_timeout_minutes
        self.workers = []
        self.is_running = False

    async def start(self):
        """Start all workers in the pool."""
        self.is_running = True
        print(f"[WorkerPool] Starting {self.num_workers} workers...")
        
        for i in range(self.num_workers):
            worker_id = f"W{i+1}"
            worker_task = asyncio.create_task(self._worker(worker_id))
            self.workers.append(worker_task)
            print(f"[WorkerPool] Started worker {worker_id}")

    async def stop(self):
        """Stop all workers gracefully."""
        self.is_running = False
        print("[WorkerPool] Stopping all workers...")
        
        # Cancel all worker tasks
        for worker in self.workers:
            worker.cancel()
        
        # Wait for all workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)
        print("[WorkerPool] All workers stopped")

    async def _acquire_task_lock(self, video_id: str, worker_id: str) -> bool:
        """
        Attempt to acquire distributed lock for a video using MongoDB atomic operation.
        
        Args:
            video_id: MongoDB ObjectId of the video
            worker_id: ID of the worker attempting to acquire lock
            
        Returns:
            True if lock was acquired, False otherwise
        """
        now = datetime.utcnow()
        lock_timeout = now - timedelta(minutes=self.lock_timeout_minutes)
        
        # Try to acquire lock using atomic findOneAndUpdate
        result = await self.db.videos.find_one_and_update(
            {
                "_id": ObjectId(video_id),
                "status": {"$in": ["pending", "failed"]},
                # Only acquire if not locked OR lock is expired
                "$or": [
                    {"processing_worker_id": None},
                    {"processing_started_at": {"$lt": lock_timeout}}
                ]
            },
            {
                "$set": {
                    "status": "processing",
                    "processing_worker_id": worker_id,
                    "processing_started_at": now,
                    "lock_acquired_at": now,
                    "updated_at": now
                }
            },
            return_document=False  # Return original document
        )
        
        return result is not None

    async def _release_task_lock(self, video_id: str):
        """
        Release distributed lock for a video.
        
        Args:
            video_id: MongoDB ObjectId of the video
        """
        await self.db.videos.update_one(
            {"_id": ObjectId(video_id)},
            {
                "$set": {
                    "processing_worker_id": None,
                    "processing_started_at": None,
                    "lock_acquired_at": None,
                    "updated_at": datetime.utcnow()
                }
            }
        )

    async def _worker(self, worker_id: str):
        """
        Worker that processes jobs from the queue.
        
        Args:
            worker_id: Unique identifier for this worker
        """
        while self.is_running:
            try:
                # Get job from queue
                video_id = await job_queue.get()
                
                try:
                    print(f"[{worker_id}] Attempting to process video {video_id}...")
                    
                    # Try to acquire distributed lock
                    lock_acquired = await self._acquire_task_lock(video_id, worker_id)
                    
                    if not lock_acquired:
                        print(f"[{worker_id}] Could not acquire lock for video {video_id} (already processing or invalid status)")
                        continue
                    
                    print(f"[{worker_id}] Lock acquired, processing video {video_id}...")
                    
                    # Process the video
                    video_service = VideoService(video_id=video_id, db=self.db)
                    try:
                        await video_service.process_video()
                        print(f"[{worker_id}] Successfully processed video {video_id}")
                    except Exception as e:
                        print(f"[{worker_id}] Error processing video {video_id}: {e}")
                        await video_service.update_video_status("failed", str(e))
                    
                    # Release lock (status is already updated by video_service)
                    await self._release_task_lock(video_id)
                    
                finally:
                    # Remove from active tasks
                    async with task_lock:
                        active_tasks.discard(video_id)
                    
                    # Mark task as done in queue
                    job_queue.task_done()
                    
            except asyncio.CancelledError:
                print(f"[{worker_id}] Worker cancelled")
                break
            except Exception as e:
                print(f"[{worker_id}] Unexpected error: {e}")
                await asyncio.sleep(1)  # Brief pause before continuing


async def add_task(video_id: str) -> bool:
    """
    Add a video processing task to the queue with duplicate prevention.
    
    Args:
        video_id: MongoDB ObjectId of the video
        
    Returns:
        True if task was added, False if already queued/processing
    """
    async with task_lock:
        if video_id in active_tasks:
            print(f"[TaskQueue] Video {video_id} already queued/processing, skipping duplicate")
            return False
        
        # Add to active tasks set
        active_tasks.add(video_id)
    
    # Add to queue
    await job_queue.put(video_id)
    print(f"[TaskQueue] Added video {video_id} to queue")
    return True


async def retry_worker(db):
    """
    Periodic worker that checks for failed videos ready to retry.
    Runs every 10 minutes.
    """
    retry_service = RetryService(db, retry_interval_minutes=10)
    
    while True:
        try:
            # Wait 10 minutes between checks
            await asyncio.sleep(600)  # 600 seconds = 10 minutes
            
            print("[RetryWorker] Checking for videos ready to retry...")
            
            # Get videos ready for retry (excluding currently processing ones)
            videos_to_retry = await retry_service.get_videos_ready_for_retry()
            
            if videos_to_retry:
                print(f"[RetryWorker] Found {len(videos_to_retry)} videos ready to retry")
                
                for video in videos_to_retry:
                    video_id = str(video._id) if video._id else str(video.id)
                    
                    # Skip if video_id is invalid
                    if not video_id or video_id == "None":
                        print(f"[RetryWorker] Skipping video with invalid ID: {video_id}")
                        continue
                    
                    # Check if already being processed
                    if video.processing_worker_id:
                        print(f"[RetryWorker] Skipping video {video_id} - currently being processed by {video.processing_worker_id}")
                        continue
                    
                    # Add to queue (with duplicate check)
                    added = await add_task(video_id)
                    if added:
                        print(f"[RetryWorker] Queued video {video_id} for retry (attempt {video.retry_count + 1}/{video.max_retries})")
            else:
                print("[RetryWorker] No videos ready for retry")
            
            # Log retry statistics
            stats = await retry_service.get_retry_statistics()
            print(f"[RetryWorker] Stats: {stats}")
            
        except Exception as e:
            print(f"[RetryWorker] Error in retry worker: {e}")
            # Continue running even if there's an error
            await asyncio.sleep(60)  # Wait 1 minute before trying again


async def cleanup_stuck_tasks(db):
    """
    Periodic cleanup worker that releases locks for stuck tasks.
    Runs every 5 minutes.
    """
    while True:
        try:
            await asyncio.sleep(300)  # 5 minutes
            
            print("[CleanupWorker] Checking for stuck tasks...")
            
            # Find tasks stuck in processing for > 5 minutes
            timeout = datetime.utcnow() - timedelta(minutes=5)
            
            result = await db.videos.update_many(
                {
                    "status": "processing",
                    "processing_started_at": {"$lt": timeout}
                },
                {
                    "$set": {
                        "status": "failed",
                        "processing_error": "Task timeout - exceeded 5 minutes",
                        "processing_worker_id": None,
                        "processing_started_at": None,
                        "lock_acquired_at": None,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count > 0:
                print(f"[CleanupWorker] Released {result.modified_count} stuck tasks")
            
        except Exception as e:
            print(f"[CleanupWorker] Error in cleanup worker: {e}")
            await asyncio.sleep(60)


# Global worker pool instance
worker_pool: WorkerPool = None


async def start_worker_pool(db, num_workers: int = 3):
    """
    Start the worker pool.
    
    Args:
        db: MongoDB database instance
        num_workers: Number of concurrent workers
    """
    global worker_pool
    worker_pool = WorkerPool(db, num_workers=num_workers)
    await worker_pool.start()


async def stop_worker_pool():
    """Stop the worker pool gracefully."""
    global worker_pool
    if worker_pool:
        await worker_pool.stop()
