"use client";
import { Button } from "@/components/ui/button";
import { DialogHeader } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

import React, { ComponentProps, Fragment, useContext } from "react";
import { FC, PropsWithChildren, useState, createContext } from "react";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";

type VideoModel = {
  openVideoModel: () => void;
  closeVideoModel: () => void;
  isVideoModelOpen: boolean;
};

export const VideoModelContext = createContext<VideoModel>({
  openVideoModel: () => {},
  closeVideoModel: () => {},
  isVideoModelOpen: false,
});

const VideoModelProvider: FC<PropsWithChildren<{}>> = ({ children }) => {
  const [ShowModel, setShowModel] = useState<boolean>(false);

  return (
    <VideoModelContext.Provider
      value={{
        openVideoModel: () => setShowModel(true),
        closeVideoModel: () => setShowModel(false),
        isVideoModelOpen: ShowModel,
      }}
    >
      <Fragment>{children}</Fragment>

      <Dialog open={ShowModel} onOpenChange={setShowModel}>
        <DialogContent className="sm:max-w-[425px] z-50">
          <DialogHeader>
            <DialogTitle>Add Video</DialogTitle>
            <DialogDescription>Add a new video to summarize.</DialogDescription>
          </DialogHeader>
          <VideoModelForm />
        </DialogContent>
      </Dialog>
    </VideoModelContext.Provider>
  );
};

export default VideoModelProvider;

function VideoModelForm({ className }: ComponentProps<"form">) {
  const [videolink, setVideolink] = useState<string>("");
  const { closeVideoModel } = useContext(VideoModelContext);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const regex =
      /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})/;
    const match = regex.exec(videolink);
    if (match) {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/videos`,
          {
            method: "POST",
            body: JSON.stringify({ url: videolink }),
          }
        );
        if (!res.ok) throw Error("Video Already Exist");
        toast.info("Video Added Successfully");
        closeVideoModel();
      } catch (error) {
        toast.error("Video Already Exist");
      }
    } else {
      toast.error("Invalid Youtube Link");
    }
  }

  return (
    <form
      className={cn("grid items-start gap-6", className)}
      onSubmit={handleSubmit}
    >
      <div className="grid gap-3">
        <Label htmlFor="link">Youtube Link</Label>
        <Input
          id="link"
          placeholder="Enter Youtube Link"
          value={videolink}
          onChange={(e) => setVideolink(e.target.value)}
        />
      </div>
      <Button type="submit">Add Video</Button>
    </form>
  );
}
