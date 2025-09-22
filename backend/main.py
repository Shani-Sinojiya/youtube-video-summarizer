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
from worker.main import worker

# Load environment variables
load_dotenv()

# Verify required environment variables
required_env_vars = ["MONGODB_URL", "DATABASE_NAME", "SECRET_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    await MongoDB.connect()

    asyncio.create_task(worker("W1", db=MongoDB.db))

    yield
    # Shutdown
    await MongoDB.close()

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
