import { NextResponse } from "next/server";
import { getRefreshPairs, sortPairsByFetchedAt, refreshWithinBudget } from "@/lib/ebayRefresh";
import { deleteExpiredConsentEvents } from "@/lib/consentRetention";

// Hits the eBay Browse API and writes Turso → Node runtime, never static.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

const BUDGET_MS = 45_000;

/**
 * Refresh cached sealed-box offers as a time-budgeted walk: process (set,format)
 * pairs ordered by fetched_at ascending (never-fetched first), stop after 45 s of
 * wall time, report how many refreshed and how many remain. Measured ~73 pairs
 * per run (eBay ~0.5 s/call), so the two daily crons (09:00, 10:00 UTC) clear
 * ~146 of 168 pairs/day; the read model's 36 h staleness window covers the rest.
 * Add a third window to raise coverage / restore a 24 h window.
 *
 * Guarded by `Authorization: Bearer <CRON_SECRET>` (Vercel sends this on
 * scheduled invocations when CRON_SECRET is set). `?limit=N` caps sets (tests).
 */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.get("authorization");
  if (!secret || auth !== `Bearer ${secret}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const url = new URL(req.url);
  const limitParam = url.searchParams.get("limit");
  const limitSets = limitParam ? Math.max(1, parseInt(limitParam, 10) || 0) : undefined;

  const { pairs } = await getRefreshPairs({ limitSets });
  const ordered = await sortPairsByFetchedAt(pairs);
  const result = await refreshWithinBudget(ordered, { budgetMs: BUDGET_MS });

  // Piggyback the 24-month consent-log retention sweep on the 09:00 UTC run
  // (scheduled with ?cleanup=1 in vercel.json). Fully guarded: any failure here
  // is swallowed so it can never affect the offers walk or the response.
  let consentCleanup: number | null = null;
  if (url.searchParams.get("cleanup") === "1") {
    try {
      consentCleanup = await deleteExpiredConsentEvents();
    } catch (err) {
      console.error("[cron] consent_events cleanup failed (non-fatal):", err);
    }
  }

  return NextResponse.json({ ...result, total: pairs.length, consentCleanup });
}
