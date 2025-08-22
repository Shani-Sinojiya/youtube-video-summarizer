import re
from urllib.parse import urlparse, parse_qs


class YouTubeParser:
    """
    A parser to extract YouTube video IDs from different types of YouTube URLs.
    Supported formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/embed/VIDEO_ID
    - https://youtube.com/v/VIDEO_ID
    - https://youtube.com/shorts/VIDEO_ID
    - With extra query params (like &t=60s etc.)
    """

    YT_DOMAINS = {"youtube.com", "www.youtube.com",
                  "m.youtube.com", "youtu.be"}

    def __init__(self, url: str):
        self.url = url.strip()
        self.video_id = self._extract_id()

    def _extract_id(self):
        parsed_url = urlparse(self.url)

        # Handle youtu.be short links
        if parsed_url.netloc == "youtu.be":
            return parsed_url.path.lstrip("/")

        # Handle youtube.com/watch?v=VIDEO_ID
        if "watch" in parsed_url.path:
            qs = parse_qs(parsed_url.query)
            return qs.get("v", [None])[0]

        # Handle embed, v, shorts
        patterns = [
            r"/embed/([a-zA-Z0-9_-]{11})",
            r"/v/([a-zA-Z0-9_-]{11})",
            r"/shorts/([a-zA-Z0-9_-]{11})"
        ]
        for pattern in patterns:
            match = re.search(pattern, parsed_url.path)
            if match:
                return match.group(1)

        return None

    def get_video_id(self):
        return self.video_id
