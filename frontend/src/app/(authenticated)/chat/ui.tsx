"use client";

import { useContext, useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/ui/command";
import { Plus, Send, X, Loader2 } from "lucide-react";
import { VideoListContext } from "@/contexts/videolist";
import { toast } from "sonner";
import { useRouter, useSearchParams } from "next/navigation";

type Video = {
  id: string;
  title: string;
};

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
  const [isSending, setIsSending] = useState<boolean>(false);
  const searchParam = useSearchParams();
  const router = useRouter();
  const videolist = useContext(VideoListContext);

  useEffect(() => {
    const id = searchParam.get("id");
    if (id && videolist?.videos && !selectedVideo) {
      const video = videolist.videos.find((v) => v.youtube_id === id);
      if (video) {
        setSelectedVideo({
          id: video.youtube_id,
          title: video.title,
        });
      }
    }
  }, [searchParam, videolist?.videos, selectedVideo]);

  const handleSend = async () => {
    if (!selectedVideo) {
      toast.warning("Please select a video before sending.");
      return;
    }
    if (!message.trim()) return;

    try {
      setIsSending(true);

      // Example: call your backend API
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          video_id: selectedVideo.id,
          question: message,
        }),
      });

      if (!res.ok) throw new Error("Failed to send message");

      const { sessionId } = await res.json();

      router.replace(`/chat/${selectedVideo.id}/${sessionId}`);

      setMessage("");
    } catch (err: any) {
      toast.error(err.message || "Something went wrong");
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-full bg-background">
      {/* Welcome Text */}
      <h1 className="text-lg font-medium text-muted-foreground mb-6">
        Good to see you, Buddy.
      </h1>

      {/* Input Box */}
      <div className="flex w-full max-w-xl items-center rounded-full bg-muted px-3 py-2 shadow-sm">
        {/* Plus Button with Video Selector */}
        <Popover>
          <PopoverTrigger asChild>
            <Button
              size="icon"
              variant="ghost"
              className="rounded-full hover:bg-accent"
            >
              <Plus className="h-5 w-5" />
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-64 p-0">
            <Command>
              <CommandInput placeholder="Search video..." />
              <CommandEmpty>No video found.</CommandEmpty>
              <CommandGroup>
                {videolist?.videos
                  ?.filter((v) => v.status === "completed")
                  .map((video) => (
                    <CommandItem
                      key={video.youtube_id}
                      onSelect={() =>
                        setSelectedVideo({
                          id: video.youtube_id,
                          title: video.title,
                        })
                      }
                    >
                      {video.title}
                    </CommandItem>
                  ))}
              </CommandGroup>
            </Command>
          </PopoverContent>
        </Popover>

        {/* Input & Video Badge */}
        <div className="flex items-center flex-1 gap-2 overflow-hidden">
          {selectedVideo && (
            <div className="flex items-center bg-accent text-accent-foreground px-2 py-1 rounded-md text-sm max-w-[50%] truncate">
              🎬 <span className="ml-1 truncate">{selectedVideo.title}</span>
              <button
                onClick={() => setSelectedVideo(null)}
                className="ml-1 hover:text-destructive"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          )}

          <Input
            type="text"
            placeholder="Ask anything"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            className="flex-1 border-0 !bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 text-base"
          />
        </div>

        {/* Send Button */}
        <Button
          size="icon"
          variant="ghost"
          className="rounded-full hover:bg-accent"
          onClick={handleSend}
          disabled={isSending}
        >
          {isSending ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <Send className="h-5 w-5" />
          )}
        </Button>
      </div>
    </div>
  );
}
