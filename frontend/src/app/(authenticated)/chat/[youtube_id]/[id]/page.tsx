import { auth } from "@/auth";
import { notFound, redirect } from "next/navigation";
import React from "react";
import ChatPage, { message } from "./ui";

export const dynamic = "force-dynamic";
export const revalidate = 0;
export const fetchCache = "force-no-store";

const Page = async ({
  params,
}: {
  params: Promise<{ id: string; youtube_id: string }>;
}) => {
  const session = await auth();

  if (!session) {
    return redirect("/login");
  }

  const { id, youtube_id } = await params;

  const res = await fetch(`${process.env.API_URL}/chat/history/${id}`, {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session.user.image}`,
    },
  });

  if (res.status == 200) {
    const chat = await res.json();

    let chats: Array<message> = [];

    for (const c of chat.history) {
      chats.push({
        message: c.content as string,
        name: "You",
        sender: c.type == "ai" ? "bot" : "user",
      });
    }

    return <ChatPage chats={chats} chat_id={id} youtube_id={youtube_id} />;
  } else notFound();
};

export default Page;
