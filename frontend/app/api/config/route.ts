import { NextResponse } from "next/server";

export async function GET() {
  // Read from server-side environment variable (without NEXT_PUBLIC_ prefix)
  const apiUrl = process.env.API_URL || "http://localhost:8001";

  return NextResponse.json({
    apiUrl,
  });
}
