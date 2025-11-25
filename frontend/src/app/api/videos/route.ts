import { auth } from "@/auth";
import { NextRequest, NextResponse } from "next/server";

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

    const res = await fetch(`${process.env.API_URL}/video`, {
      headers: {
        Authorization: `Bearer ${session.user.image}`,
      },
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      console.error("Backend error fetching videos:", res.status, errorData);
      return NextResponse.json(
        { error: errorData.detail || "Failed to fetch videos" },
        { status: res.status }
      );
    }

    const data = await res.json();

    // Check if the data object is empty or not an array
    if (!data || !Array.isArray(data)) {
      // If it's an empty object or null, return empty array
      if (data && Object.keys(data).length === 0) {
        return NextResponse.json([]);
      }
      // If it's something else (unexpected), log it and return empty
      console.warn("Unexpected data format from backend:", data);
      return NextResponse.json([]);
    }

    return NextResponse.json([...data].reverse());
  } catch (error) {
    console.error("Error fetching chats:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}

export async function POST(req: NextRequest) {
  try {
    const session = await auth();

    if (!session || !session.user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const { url } = await req.json();

    const res = await fetch(`${process.env.API_URL}/video/upload`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${session.user.image}`,
        "Content-type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorData.detail || "Failed to upload video" },
        { status: res.status }
      );
    }

    return NextResponse.json({ message: "Uploading Successfully" });
  } catch (error) {
    console.error("Error fetching chats:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
