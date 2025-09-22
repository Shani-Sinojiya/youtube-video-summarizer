import { auth } from "@/auth";
import { NextRequest, NextResponse } from "next/server";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const session = await auth();

    if (!session || !session.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    const { id } = await params;

    // In a real application, you would fetch this from a database
    const res = await fetch(`${process.env.API_URL}/chat/history/${id}`, {
      // method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.user.image}`,
      },
      // body: JSON.stringify({ sessionId: id }),
    });

    const chat = await res.json();

    // Make sure the response always has a messages array
    if (!chat || typeof chat !== "object") {
      return NextResponse.json({
        id,
        messages: [],
      });
    }

    let chats = [];

    for (const c of chat.history) {
      chats.push({ message: c.content as string, role: c.type });
    }

    return NextResponse.json({ id, messages: chats });
  } catch {
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
