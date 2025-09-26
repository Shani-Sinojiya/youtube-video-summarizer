"use client";

import { VideoListContext } from "@/contexts/videolist";
import Link from "next/link";
import { useContext } from "react";
import { Video, VideoGridProps } from "./types";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

const UI = () => {
  const videolist = useContext(VideoListContext);
  const router = useRouter();

  return (
    <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
      <VideoGrid
        videos={videolist?.videos || []}
        onChat={(video_id) => {
          router.replace("/chat?id=" + video_id);
        }}
      />
    </div>
  );
};

export default UI;

const VideoGrid: React.FC<VideoGridProps> = ({ videos, onChat }) => {
  const getStatusClass = (status: Video["status"]) => {
    switch (status) {
      case "pending":
        return "bg-neutral-600 dark:bg-neutral-600 text-neutral-200 dark:text-neutral-200";
      case "processing":
        return "bg-yellow-600 dark:bg-yellow-600 text-neutral-100 dark:text-neutral-100";
      case "completed":
        return "bg-green-600 dark:bg-green-600 text-neutral-100 dark:text-neutral-100";
      case "failed":
        return "bg-red-600 dark:bg-red-600 text-neutral-100 dark:text-neutral-100";
      default:
        return "bg-neutral-600 dark:bg-neutral-600 text-neutral-200 dark:text-neutral-200";
    }
  };

  return (
    <div className="px-4 lg:px-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 w-full">
      {videos.map((video) => (
        <div
          key={video.youtube_id}
          className="group flex flex-col bg-white dark:bg-neutral-800 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-transform duration-300 hover:scale-[1.02] border border-neutral-200 dark:border-neutral-700"
        >
          {/* Thumbnail */}
          <div className="relative w-full h-48 overflow-hidden">
            <img
              src={video.thumbnail_url}
              alt={video.title}
              className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
            />

            {/* Status Badge */}
            <div
              className={`absolute top-2 left-2 text-xs px-2 py-1 rounded-md capitalize ${getStatusClass(
                video.status
              )}`}
            >
              {video.status}
            </div>

            {/* Duration Badge */}
            <div className="absolute bottom-2 right-2 text-xs px-2 py-1 rounded-md bg-black/70 dark:bg-neutral-700/70 text-white dark:text-neutral-200">
              {Math.floor(video.duration_seconds / 60)}m{" "}
              {video.duration_seconds % 60}s
            </div>
          </div>

          {/* Content */}
          <div className="flex flex-col p-4 gap-2 flex-1">
            <h3
              className="text-base font-semibold line-clamp-2 text-neutral-900 dark:text-neutral-100"
              title={video.title}
            >
              {video.title}
            </h3>
            <p
              className="text-sm text-neutral-600 dark:text-neutral-400 line-clamp-3"
              title={video.description}
            >
              {video.description}
            </p>

            <div className="flex flex-col gap-1 text-xs text-neutral-500 dark:text-neutral-400 mt-auto">
              <span>Views: {video.view_count.toLocaleString()}</span>
              <Link
                href={video.channel_url}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline text-neutral-700 dark:text-neutral-300"
              >
                Uploader: {video.uploader}
              </Link>
            </div>

            {/* Chat Button */}
            <Button
              onClick={() => onChat(video.youtube_id)}
              variant={"outline"}
              className="mt-2"
            >
              💬 Chat with this video
            </Button>
          </div>
        </div>
      ))}
    </div>
  );
};
