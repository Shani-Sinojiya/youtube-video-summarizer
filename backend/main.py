"""
Main entry point for the YouTube Video Summarizer FastAPI backend.
"""

import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.mongodb import MongoDB
from routes import auth, video, chat
from worker.main import start_worker_pool, stop_worker_pool, retry_worker, cleanup_stuck_tasks

# Load environment variables
load_dotenv()

# Verify required environment variables
required_env_vars = ["MONGODB_URL",
                     "DATABASE_NAME", "SECRET_KEY", "MONGODB_URI", "GOOGLE_API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    await MongoDB.connect()

    # Verify Google API
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
        await llm.ainvoke("test")
        print("[Startup] ✅ Google API connection verified")
    except Exception as e:
        print(f"[Startup] ❌ Google API connection failed: {e}")
        # We don't raise here to allow app to start, but logs will show error

    # Get number of workers from environment (default: 3)
    num_workers = int(os.getenv("NUM_WORKERS", "3"))
    
    # Start worker pool
    await start_worker_pool(db=MongoDB.db, num_workers=num_workers)
    print(f"[Startup] Started worker pool with {num_workers} workers")
    
    # Start retry worker (runs every 10 minutes)
    asyncio.create_task(retry_worker(db=MongoDB.db))
    print("[Startup] Started retry worker")
    
    # Start cleanup worker for stuck tasks (runs every 5 minutes)
    asyncio.create_task(cleanup_stuck_tasks(db=MongoDB.db))
    print("[Startup] Started cleanup worker")

    yield
    
    # Shutdown
    print("[Shutdown] Stopping worker pool...")
    await stop_worker_pool()
    await MongoDB.close()
    print("[Shutdown] Complete")

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Video Summarizer API",
    description="API for multilingual video summarization and chat using Gemini 2.0",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(video.router, prefix="/api", tags=["videos"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
