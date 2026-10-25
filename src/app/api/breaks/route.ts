import { NextResponse } from "next/server";
import { rawQuery } from "@/lib/db";
import { getBreaksForSet, refreshSetBreaks, isStale, WHATNOT_INVITE_URL, type BreaksPayload } from "@/lib/breaks/refresh";

// Hits the eBay Browse API and writes Turso on a stale set → Node runtime, never
// static. The client components on the set / athlete pages fetch this directly
// (those pages are cached), so the CDN layer (below) absorbs repeat views.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 15;

const REFRESH_TIMEOUT_MS = 8_000;

function disabled(setSlug: string): BreaksPayload {
  return {
    enabled: false, setSlug, setName: "", breaks: [], searchUrl: null,
    refreshedRelative: null, disclosure: "", whatnotUrl: WHATNOT_INVITE_URL, playerName: null,
  };
}

/**
 * GET /api/breaks?set=<slug|id>[&player=<id>] → grouped live break spots.
 * Gated by LIVE_BREAKS_ENABLED (default off). Refreshes the set inline when its
 * cache is stale (>6 h) or empty, bounded by an 8 s eBay timeout; otherwise serves
 * the cached listings. The response is CDN-cacheable for 15 min (SWR 1 h).
 */
export async function GET(req: Request) {
  const url = new URL(req.url);
  const setParam = (url.searchParams.get("set") ?? "").trim();
  const playerParam = url.searchParams.get("player");

  if (process.env.LIVE_BREAKS_ENABLED !== "true") {
    return NextResponse.json(disabled(setParam), { headers: { "Cache-Control": "no-store" } });
  }
  if (!setParam) {
    return NextResponse.json({ error: "Missing ?set" }, { status: 400, headers: { "Cache-Control": "no-store" } });
  }

  // Resolve set by slug, else numeric id.
  let setRow: { id: number; name: string; slug: string | null } | undefined;
  try {
    setRow = await rawQuery.get<{ id: number; name: string; slug: string | null }>(
      "SELECT id, name, slug FROM sets WHERE slug = ?", setParam
    );
  } catch { /* slug column may be absent pre-migration */ }
  if (!setRow && /^\d+$/.test(setParam)) {
    setRow = await rawQuery.get<{ id: number; name: string; slug: string | null }>(
      "SELECT id, name, slug FROM sets WHERE id = ?", parseInt(setParam, 10)
    );
  }
  if (!setRow) {
    return NextResponse.json({ error: "Set not found" }, { status: 404, headers: { "Cache-Control": "no-store" } });
  }

  const setSlug = setRow.slug ?? String(setRow.id);
  let playerId: number | undefined;
  let playerName: string | null = null;
  if (playerParam && /^\d+$/.test(playerParam)) {
    playerId = parseInt(playerParam, 10);
    const p = await rawQuery.get<{ name: string }>(
      "SELECT name FROM players WHERE id = ? AND set_id = ?", playerId, setRow.id
    );
    if (!p) playerId = undefined; // player not in this set → fall back to set-wide
    else playerName = p.name;
  }

  // On-demand refresh when stale/empty (bounded). Never fatal: fall through to
  // whatever is cached if the refresh errors.
  try {
    const state = await rawQuery.get<{ last_fetched_at: string | null }>(
      "SELECT last_fetched_at FROM break_refresh_state WHERE set_id = ?", setRow.id
    );
    if (isStale(state?.last_fetched_at)) {
      await refreshSetBreaks(
        { setId: setRow.id, slug: setSlug, setName: setRow.name },
        { timeoutMs: REFRESH_TIMEOUT_MS }
      );
    }
  } catch { /* serve cached */ }

  const payload = await getBreaksForSet({
    setId: setRow.id, setSlug, setName: setRow.name, playerId, playerName,
    max: playerId != null ? 8 : 12,
  });

  return NextResponse.json(payload, {
    headers: { "Cache-Control": "public, s-maxage=900, stale-while-revalidate=3600" },
  });
}
