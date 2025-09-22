"use client";

import { useState, useRef, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

type ChatBubbleProps = {
  message: string;
  sender?: "user" | "bot";
  avatar?: string;
  name?: string;
};

function ChatBubble({
  message,
  sender = "user",
  avatar,
  name,
}: ChatBubbleProps) {
  const isUser = sender === "user";

  return (
    <div
      className={cn(
        "flex items-end gap-2",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      {!isUser && (
        <Avatar className="w-8 h-8">
          <AvatarImage src={avatar} />
          <AvatarFallback>A</AvatarFallback>
        </Avatar>
      )}

      <div
        className={cn(
          "max-w-xs rounded-2xl px-4 py-2 text-sm shadow",
          isUser
            ? "bg-primary text-primary-foreground rounded-br-none"
            : "bg-muted text-muted-foreground rounded-bl-none"
        )}
      >
        {message}
      </div>

      {isUser && (
        <Avatar className="w-8 h-8">
          <AvatarImage src={avatar} />
          <AvatarFallback>{name?.[0] ?? "U"}</AvatarFallback>
        </Avatar>
      )}
    </div>
  );
}

export type message = {
  sender: string;
  message: string;
  name: string;
};

export default function ChatPage({
  chats,
  youtube_id,
  chat_id,
}: {
  youtube_id: string;
  chat_id: string;
  chats: Array<message>;
}) {
  const [messages, setMessages] = useState<Array<message>>(chats);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState<boolean>(false);

  const scrollRef = useRef<HTMLDivElement>(null);

  // auto scroll to bottom when messages update
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (isSending) {
      toast.warning("Message is in processing", {
        description: "Please wait until it's sent.",
      });
      return;
    }
    if (!input.trim()) return;

    const question = input;
    setInput("");
    setIsSending(true);

    // add user message
    setMessages((prev) => [
      ...prev,
      { sender: "user", message: question, name: "You" },
    ]);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          video_id: youtube_id,
          chatid: chat_id,
        }),
      });

      if (!res.ok) throw new Error("Answer generation error");

      const { answer } = await res.json();

      // add bot message
      setMessages((prev) => [
        ...prev,
        { sender: "bot", message: answer, name: "ai" },
      ]);
    } catch (err: any) {
      toast.error(err.message ?? "Something went wrong");
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-64px)]">
      {/* Chat area */}
      <ScrollArea className="flex-1 bg-muted/20 h-[calc(100vh-64px-64px)]">
        <div ref={scrollRef} className="p-4 flex flex-col gap-4">
          {messages.map((msg, i) => (
            <ChatBubble
              key={i}
              sender={msg.sender as "user" | "bot"}
              message={msg.message}
              name={msg.name}
            />
          ))}
        </div>
      </ScrollArea>

      {/* Input area (fixed at bottom) */}
      <footer className="p-4 border-t bg-background">
        <div className="flex items-center gap-2">
          <Input
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <Button onClick={sendMessage} disabled={isSending}>
            Send
          </Button>
        </div>
      </footer>
    </div>
  );
}
