import { NextResponse } from "next/server";
import { revalidatePath } from "next/cache";
import { getRefreshPairs, sortPairsByFetchedAt, refreshWithinBudget } from "@/lib/ebayRefresh";
import { getBreakRefreshSets, sortSetsByFetchedAt, refreshBreaksWithinBudget } from "@/lib/breaks/refresh";
import { deleteExpiredConsentEvents } from "@/lib/consentRetention";

// Hits the eBay Browse API and writes Turso → Node runtime, never static.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60; // Hobby plan cap.

// Both daily runs walk sealed-box offers (30 s); the 10:00 run (vercel.json
// `?breaks=1`) adds a 15 s break-spots pass after it, keeping the heaviest run
// at ~45 s under the 60 s cap. 09:00 stays light (offers + consent sweep).
const BUDGET_MS = 30_000;
const BREAKS_BUDGET_MS = 15_000;

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

  // Set pages are cached indefinitely (revalidate = false), so on-demand revalidate
  // exactly the set pages whose sealed-box offers changed this run (a few dozen/day)
  // — otherwise refreshed offers would never surface.
  for (const slug of result.refreshedSlugs) {
    try {
      revalidatePath(`/sets/${slug}`, "page");
    } catch (err) {
      console.error(`[cron] revalidate /sets/${slug} failed (non-fatal):`, err);
    }
  }

  // Live break spots (category 261334). Runs on the 10:00 cron only (`?breaks=1`)
  // so it isn't done twice, and gated by LIVE_BREAKS_ENABLED (default off). Own
  // time budget after the offers walk; fully guarded so a breaks failure can
  // never affect the offers response. Revalidate the set pages whose breaks
  // changed (their client component re-fetches, but revalidating keeps the
  // server-rendered shell current alongside the sealed-box refresh above).
  let breaks: Awaited<ReturnType<typeof refreshBreaksWithinBudget>> | null = null;
  if (url.searchParams.get("breaks") === "1" && process.env.LIVE_BREAKS_ENABLED === "true") {
    try {
      const sets = await getBreakRefreshSets({ limitSets });
      const orderedSets = await sortSetsByFetchedAt(sets);
      breaks = await refreshBreaksWithinBudget(orderedSets, { budgetMs: BREAKS_BUDGET_MS });
      for (const slug of breaks.refreshedSlugs) {
        try { revalidatePath(`/sets/${slug}`, "page"); } catch { /* non-fatal */ }
      }
    } catch (err) {
      console.error("[cron] break_listings refresh failed (non-fatal):", err);
    }
  }

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

  return NextResponse.json({ ...result, revalidated: result.refreshedSlugs.length, total: pairs.length, breaks, consentCleanup });
}
