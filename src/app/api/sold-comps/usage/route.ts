import { NextResponse } from "next/server";
import { rawQuery } from "@/lib/db";
import { dailyCap } from "@/lib/soldComps";

// Reads Turso → Node runtime, never static.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/**
 * Read-only admin visibility into today's sold-comps usage. Guarded by the same
 * Bearer CRON_SECRET as the cron routes. Returns today's fresh-call count, the
 * configured daily cap, and the last-seen X-Usage/X-Credit/X-RateLimit headers.
 */
export async function GET(req: Request) {
  if (process.env.SOLD_COMPS_ENABLED !== "true") {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.get("authorization");
  if (!secret || auth !== `Bearer ${secret}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const today = new Date().toISOString().slice(0, 10);
  const row = await rawQuery.get<{ calls: number; credits_used_estimate: number; last_x_usage_json: string | null }>(
    `SELECT calls, credits_used_estimate, last_x_usage_json FROM sold_comps_usage WHERE day = ?`,
    today
  );
  let lastXUsage: Record<string, string> | null = null;
  try { lastXUsage = row?.last_x_usage_json ? JSON.parse(row.last_x_usage_json) : null; } catch { lastXUsage = null; }

  return NextResponse.json({
    day: today,
    calls: row?.calls ?? 0,
    cap: dailyCap(),
    creditsUsedEstimate: row?.credits_used_estimate ?? 0,
    lastXUsage,
  });
}
