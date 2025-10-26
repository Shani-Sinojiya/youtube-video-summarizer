import yt_dlp
import json
from typing import Dict, Optional, Any


class YouTubeInfoExtractor:
    def __init__(self, ydl_opts: Optional[Dict[str, Any]] = None):
        """Initialize the extractor with yt_dlp options."""
        self.ydl_opts = ydl_opts or {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': True,  # Continue on errors
            'no_check_certificate': True,  # Skip SSL certificate verification if needed
            # Removed format specification to avoid format-related issues
        }

    def get_info(self, url: str) -> Dict[str, Optional[str]]:
        """Extract video information without downloading the video.

        Args:
            url: YouTube video URL

        Returns:
            Dictionary containing video information

        Raises:
            Exception: If video extraction fails
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:  # type: ignore
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
            # Handle format-related errors specifically
            if "Requested format is not available" in str(e) or "Only images are available" in str(e):
                # Try with no format specified - just get basic info
                info_only_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'skip_download': True,
                    'ignoreerrors': True,
                    'no_check_certificate': True,
                    # Remove format specification entirely for problematic videos
                }

                try:
                    with yt_dlp.YoutubeDL(info_only_opts) as ydl:  # type: ignore
                        info = ydl.extract_info(url, download=False)
                        if info is None:
                            raise Exception(
                                "Video information is not available - video may be private, deleted, or restricted")

                        return {
                            "title": info.get("title"),  # type: ignore
                            "uploader": info.get("uploader"),  # type: ignore
                            # type: ignore
                            "channel_url": info.get("channel_url"),
                            "views": info.get("view_count"),  # type: ignore
                            # type: ignore
                            "duration_seconds": info.get("duration"), # type: ignore
                            # type: ignore
                            "upload_date": info.get("upload_date"),
                            # type: ignore
                            "description": info.get("description"),
                            # type: ignore
                            "video_url": info.get("webpage_url"),
                            "thumbnail": info.get("thumbnail"),  # type: ignore
                        }
                except Exception as fallback_error:
                    raise Exception(
                        f"Video information extraction failed - video may be private, deleted, or restricted: {str(fallback_error)}")
            else:
                raise Exception(f"Failed to extract video info: {str(e)}")

    def to_json(self, url: str) -> str:
        """Get video info as JSON string.

        Args:
            url: YouTube video URL

        Returns:
            JSON string representation of video information
        """
        video_info = self.get_info(url)
        return json.dumps(video_info, indent=2, ensure_ascii=False)
