import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { playerEvents } from "@/lib/schema";

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  if (!body) return NextResponse.json({ error: "invalid json" }, { status: 400 });

  const { playerId, eventType } = body;
  if (!Number.isInteger(playerId) || !["search", "view"].includes(eventType)) {
    return NextResponse.json({ error: "invalid" }, { status: 400 });
  }

  await db.insert(playerEvents).values({
    playerId,
    eventType,
    createdAt: Date.now(),
  });

  return NextResponse.json({ ok: true });
}
