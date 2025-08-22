import yt_dlp
import json
from typing import Dict, Optional


class YouTubeInfoExtractor:
    def __init__(self, ydl_opts: Optional[Dict] = None):
        """Initialize the extractor with yt_dlp options."""
        self.ydl_opts = ydl_opts or {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }

    def get_info(self, url: str) -> Dict[str, Optional[str]]:
        """Extract video information without downloading the video.

        Args:
            url: YouTube video URL

        Returns:
            Dictionary containing video information

        Raises:
            yt_dlp.DownloadError: If video extraction fails
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                return {
                    "title": info.get("title"),  # type: ignore
                    "uploader": info.get("uploader"),  # type: ignore
                    "channel_url": info.get("channel_url"),  # type: ignore
                    "views": info.get("view_count"),  # type: ignore
                    "duration_seconds": info.get("duration"),  # type: ignore
                    "upload_date": info.get("upload_date"),  # type: ignore
                    "description": info.get("description"),  # type: ignore
                    "video_url": info.get("webpage_url"),  # type: ignore
                    "thumbnail": info.get("thumbnail"),  # type: ignore
                }
        except Exception as e:
            raise yt_dlp.DownloadError(
                f"Failed to extract video info: {str(e)}")

    def to_json(self, url: str) -> str:
        """Get video info as JSON string.

        Args:
            url: YouTube video URL

        Returns:
            JSON string representation of video information
        """
        video_info = self.get_info(url)
        return json.dumps(video_info, indent=2, ensure_ascii=False)
