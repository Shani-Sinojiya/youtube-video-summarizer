import { auth } from "@/auth";
import { NextRequest, NextResponse } from "next/server";
import { v7 as uuidv7 } from "uuid";

export async function POST(request: NextRequest) {
  try {
    const session = await auth();

    if (!session || !session.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Extract message and chatId from request body
    const body = await request.json();
    const { question, chatid, video_id } = body;

    // Generate a new session ID if one wasn't provided
    const sessionId = chatid || uuidv7();

    const res = await fetch(`${process.env.API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.user.image}`,
      },
      body: JSON.stringify({
        chat_id: sessionId,
        question,
        video_id,
      }),
    });

    const data = await res.json();

    const { answer } = data;

    return NextResponse.json({ answer, sessionId });
  } catch {
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
