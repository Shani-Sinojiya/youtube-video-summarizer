import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const revalidate = 0; // Disable caching for this route
export const runtime = "edge"; // Use edge runtime for better performance

export async function POST(request: NextRequest) {
  const { hash } = await request.json();

  if (!hash) {
    return NextResponse.json({ error: "Hash is required" }, { status: 400 });
  }

  try {
    const res = await fetch(
      `${process.env.API_URL}/reset-password/verify-hash`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hash }),
      }
    );

    if (!res.ok) {
      const errorData = await res.json();
      return NextResponse.json(
        { error: errorData.message || "Failed to verify token" },
        { status: res.status }
      );
    }

    const data = await res.json();

    return NextResponse.json({
      message: "Token verification successful",
      data,
    });
  } catch {
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
