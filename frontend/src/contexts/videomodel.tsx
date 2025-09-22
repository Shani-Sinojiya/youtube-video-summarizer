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

import React, { ComponentProps, Fragment } from "react";
import { FC, PropsWithChildren, useState, createContext } from "react";
import { Label } from "@/components/ui/label";

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
  return (
    <form className={cn("grid items-start gap-6", className)}>
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
