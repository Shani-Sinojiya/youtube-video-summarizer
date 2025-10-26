import { auth } from "@/auth";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic"; // Ensure this route is always dynamic
export const revalidate = 0; // Disable static generation for this route
export const fetchCache = "force-no-store"; // Disable caching for this route

export async function GET() {
  try {
    const session = await auth();

    if (!session || !session.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // console.log("Fetching chat list for user:", session.user.token);

    const res = await fetch(`${process.env.API_URL}/chat/history`, {
      // method: "POST",
      headers: {
        // "Content-Type": "application/json",
        Authorization: `Bearer ${session.user.image}`,
      },
      // body: JSON.stringify({ userid: session.user.id }),
    });

    if (!res.ok) {
      console.error("API request failed:", res.status, res.statusText);
      return NextResponse.json([]);
    }

    const data = await res.json();

    // Check if the data object is empty or has an error
    if (data.error) {
      console.log("API returned error:", data.error);
      return NextResponse.json([]);
    }

    // console.log("Fetched chats:", data);

    // Ensure chat_histories is an array before spreading
    const chatHistories = Array.isArray(data.chat_histories)
      ? data.chat_histories
      : [];

    return NextResponse.json(chatHistories);
  } catch (error) {
    console.error("Error fetching chats:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
