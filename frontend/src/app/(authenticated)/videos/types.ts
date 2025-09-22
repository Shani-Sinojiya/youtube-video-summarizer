interface Video {
  youtube_id: string;
  title: string;
  description: string;
  thumbnail_url: string;
  default_language: string;
  available_languages: string[];
  status: string;
  processing_error: any;
  created_at: string;
  updated_at: string;
  processed_at: string;
  duration_seconds: number;
  view_count: number;
  uploader: string;
  channel_url: string;
}

interface VideoGridProps {
  videos: Video[];
  onChat: (videoId: string) => void; // handler for chat button
}

export type { Video, VideoGridProps };
