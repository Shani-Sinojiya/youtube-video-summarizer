"use client";
import React, { createContext, PropsWithChildren } from "react";
import useSWR from "swr";

type VideoInfo = {
  // id: any;
  youtube_id: string;
  title: string;
  thumbnail_url: string;
  // transcripts: {};
  default_language: string;
  available_languages: Array<string>;
  status: string;
  processing_error: any;
  // vector_ids: any;
  created_at: string;
  updated_at: string;
  processed_at: string;
  description: string;
  duration_seconds: number;
  view_count: number;
  uploader: string;
  channel_url: string;
};

type VideoListContextType = {
  videos: Array<VideoInfo> | undefined;
  isLoading: boolean;
  error: any;
};

export const VideoListContext = createContext<VideoListContextType | undefined>(
  undefined
);

const VideoListProvider = ({ children }: PropsWithChildren) => {
  const { data, error, isLoading } = useSWR("/api/videos", {
    refreshInterval: 1000 * 60 * 5, // 5 minutes
    fetcher: (url: string) => fetch(url).then((res) => res.json()),
  }) as { data: VideoInfo[]; error: any; isLoading: boolean };

  console.log(data, error, isLoading);

  return (
    <VideoListContext.Provider
      value={{
        videos: data || [],
        isLoading,
        error,
      }}
    >
      {children}
    </VideoListContext.Provider>
  );
};

export default VideoListProvider;
