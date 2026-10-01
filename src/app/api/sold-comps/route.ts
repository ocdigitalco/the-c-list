import { NextResponse } from "next/server";
import { rawQuery } from "@/lib/db";
import {
  SOLD_COMPS_ENDPOINT, CACHE_TTL_DAYS, PER_IP_HOURLY_CAP, API_TIMEOUT_MS,
  dailyCap, buildKeyword, hashIp, clientIpFrom, summarizeItems, collectUsageHeaders,
  type SoldItem, type SoldSummary,
} from "@/lib/soldComps";

// Writes Turso + calls an external API → Node runtime, never static/cached.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 30;

interface Body { set_id: number; insert_set_id: number; card_number: string; player_id: number }

function flagOn(): boolean {
  return process.env.SOLD_COMPS_ENABLED === "true";
}

/** Shape a stored/computed summary for the client (State 2). */
function toClientSummary(s: {
  priceCents: number; soldAt: string | null; url: string | null; type: string | null;
  median30dCents?: number | null; count30d?: number | null; low30dCents?: number | null; high30dCents?: number | null;
}) {
  return {
    priceCents: s.priceCents,
    soldAt: s.soldAt,
    url: s.url,
    type: s.type,
    median30dCents: s.median30dCents ?? null,
    count30d: s.count30d ?? null,
    low30dCents: s.low30dCents ?? null,
    high30dCents: s.high30dCents ?? null,
  };
}

export async function POST(req: Request) {
  // Feature flag: off → the route does not exist.
  if (!flagOn()) return NextResponse.json({ error: "Not found" }, { status: 404 });
  if (!process.env.SOLD_COMPS_API_KEY) {
    return NextResponse.json({ status: "error" }, { status: 500 });
  }

  let body: Body;
  try { body = (await req.json()) as Body; } catch { return NextResponse.json({ error: "Bad request" }, { status: 400 }); }
  const setId = Number(body.set_id), insertSetId = Number(body.insert_set_id), playerId = Number(body.player_id);
  const cardNumber = typeof body.card_number === "string" ? body.card_number : "";
  if (!Number.isInteger(setId) || !Number.isInteger(insertSetId) || !Number.isInteger(playerId) || !cardNumber) {
    return NextResponse.json({ error: "Bad request" }, { status: 400 });
  }

  // Validate the tuple exists and belongs together; fetch names for the keyword.
  const appearance = await rawQuery.get<{ set_name: string; player_name: string }>(
    `SELECT s.name AS set_name, p.name AS player_name
     FROM player_appearances pa
     JOIN insert_sets i ON i.id = pa.insert_set_id
     JOIN sets s ON s.id = i.set_id
     JOIN players p ON p.id = pa.player_id
     WHERE i.set_id = ? AND pa.insert_set_id = ? AND pa.card_number = ? AND pa.player_id = ?
     LIMIT 1`,
    setId, insertSetId, cardNumber, playerId
  );
  if (!appearance) return NextResponse.json({ error: "Unknown card" }, { status: 400 });

  const cacheKey = `${setId}|${insertSetId}|${cardNumber}|${playerId}|raw`;
  const now = new Date();

  // ── Cache lookup (fresh within TTL → no API call) ────────────────────────────
  const cached = await rawQuery.get<{
    last_sold_price_cents: number | null; last_sold_at: string | null; last_sold_url: string | null; last_sold_type: string | null;
    median_30d_cents: number | null; count_30d: number | null; low_30d_cents: number | null; high_30d_cents: number | null; fetched_at: string | null;
  }>(
    `SELECT last_sold_price_cents, last_sold_at, last_sold_url, last_sold_type,
            median_30d_cents, count_30d, low_30d_cents, high_30d_cents, fetched_at
     FROM sold_comps
     WHERE set_id = ? AND insert_set_id = ? AND card_number = ? AND player_id = ? AND grade_filter = 'raw'`,
    setId, insertSetId, cardNumber, playerId
  );
  const cacheFresh = (() => {
    if (!cached?.fetched_at) return false;
    const ageMs = now.getTime() - new Date(cached.fetched_at).getTime();
    return Number.isFinite(ageMs) && ageMs < CACHE_TTL_DAYS * 24 * 60 * 60 * 1000;
  })();
  const cachedResponse = () => {
    if (!cached) return null;
    if (cached.last_sold_price_cents == null) return NextResponse.json({ status: "no_sales" });
    return NextResponse.json({
      status: "ok",
      summary: toClientSummary({
        priceCents: cached.last_sold_price_cents, soldAt: cached.last_sold_at, url: cached.last_sold_url, type: cached.last_sold_type,
        median30dCents: cached.median_30d_cents, count30d: cached.count_30d, low30dCents: cached.low_30d_cents, high30dCents: cached.high_30d_cents,
      }),
    });
  };
  if (cacheFresh) return cachedResponse()!;

  // ── Caps (checked before any fresh call) ─────────────────────────────────────
  const today = now.toISOString().slice(0, 10);
  const ipHash = hashIp(clientIpFrom(req.headers));
  // Purge >24h request log rows opportunistically.
  const cutoff24h = new Date(now.getTime() - 24 * 60 * 60 * 1000).toISOString();
  await rawQuery.run(`DELETE FROM sold_comps_requests WHERE requested_at < ?`, cutoff24h);

  const cutoff1h = new Date(now.getTime() - 60 * 60 * 1000).toISOString();
  const ipCount = await rawQuery.get<{ n: number }>(
    `SELECT COUNT(*) AS n FROM sold_comps_requests WHERE ip_hash = ? AND requested_at >= ?`,
    ipHash, cutoff1h
  );
  const usageRow = await rawQuery.get<{ calls: number }>(`SELECT calls FROM sold_comps_usage WHERE day = ?`, today);
  const overIp = (ipCount?.n ?? 0) >= PER_IP_HOURLY_CAP;
  const overDaily = (usageRow?.calls ?? 0) >= dailyCap();
  if (overIp || overDaily) {
    const c = cachedResponse();
    return c ?? NextResponse.json({ status: "capped" });
  }

  // ── Fresh call ───────────────────────────────────────────────────────────────
  const keyword = buildKeyword(appearance.set_name, appearance.player_name, cardNumber);
  const url = new URL(SOLD_COMPS_ENDPOINT);
  url.searchParams.set("keyword", keyword);
  url.searchParams.set("sold", "true");
  url.searchParams.set("exactMatch", "true");
  url.searchParams.set("hydrateBoa", "true");
  url.searchParams.set("includeCompleteListing", "true");
  url.searchParams.set("sortOrder", "endedRecently");

  async function callOnce(): Promise<Response | null> {
    const ac = new AbortController();
    const timer = setTimeout(() => ac.abort(), API_TIMEOUT_MS);
    try {
      return await fetch(url, {
        headers: { Authorization: `Bearer ${process.env.SOLD_COMPS_API_KEY}` },
        signal: ac.signal,
      });
    } catch { return null; } finally { clearTimeout(timer); }
  }

  let res = await callOnce();
  // 429: honor Retry-After once (but not for monthly quota — a retry can't help).
  if (res && res.status === 429) {
    let code: string | undefined;
    try { code = (await res.clone().json())?.code; } catch { /* ignore */ }
    const retryAfter = Number(res.headers.get("retry-after"));
    if (code !== "quota_exceeded" && Number.isFinite(retryAfter) && retryAfter > 0 && retryAfter <= 15) {
      await new Promise((r) => setTimeout(r, retryAfter * 1000));
      res = await callOnce();
    } else {
      return NextResponse.json({ status: "error" });
    }
  }
  if (!res || !res.ok) return NextResponse.json({ status: "error" });

  let payload: { items?: SoldItem[] };
  try { payload = await res.json(); } catch { return NextResponse.json({ status: "error" }); }
  const items = Array.isArray(payload.items) ? payload.items : [];
  const summary: SoldSummary | null = summarizeItems(items, now);

  // Record the (charged) fresh call: request-log row + usage increment with headers.
  const usageHeaders = JSON.stringify(collectUsageHeaders(res.headers));
  await rawQuery.run(
    `INSERT INTO sold_comps_requests (ip_hash, requested_at, cache_key) VALUES (?, ?, ?)`,
    ipHash, now.toISOString(), cacheKey
  );
  await rawQuery.run(
    `INSERT INTO sold_comps_usage (day, calls, credits_used_estimate, last_x_usage_json)
     VALUES (?, 1, 1, ?)
     ON CONFLICT(day) DO UPDATE SET calls = calls + 1, credits_used_estimate = credits_used_estimate + 1, last_x_usage_json = excluded.last_x_usage_json`,
    today, usageHeaders
  );

  // Upsert the cache row (null fields when no sales → cached so we don't re-call).
  await rawQuery.run(
    `INSERT INTO sold_comps (
       set_id, insert_set_id, card_number, player_id, grade_filter, keyword,
       last_sold_price_cents, last_sold_at, last_sold_url, last_sold_type,
       median_30d_cents, count_30d, low_30d_cents, high_30d_cents, raw_items_json, fetched_at, source
     ) VALUES (?, ?, ?, ?, 'raw', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'sold-comps')
     ON CONFLICT(set_id, insert_set_id, card_number, player_id, grade_filter) DO UPDATE SET
       keyword = excluded.keyword,
       last_sold_price_cents = excluded.last_sold_price_cents,
       last_sold_at = excluded.last_sold_at,
       last_sold_url = excluded.last_sold_url,
       last_sold_type = excluded.last_sold_type,
       median_30d_cents = excluded.median_30d_cents,
       count_30d = excluded.count_30d,
       low_30d_cents = excluded.low_30d_cents,
       high_30d_cents = excluded.high_30d_cents,
       raw_items_json = excluded.raw_items_json,
       fetched_at = excluded.fetched_at`,
    setId, insertSetId, cardNumber, playerId, keyword,
    summary?.priceCents ?? null, summary?.soldAt ?? null, summary?.url ?? null, summary?.type ?? null,
    summary?.median30dCents ?? null, summary?.count30d ?? 0, summary?.low30dCents ?? null, summary?.high30dCents ?? null,
    JSON.stringify(items), now.toISOString()
  );

  console.info(`[sold-comps] keyword="${keyword}" items=${items.length} priced=${summary ? "yes" : "no"}`);

  if (!summary) return NextResponse.json({ status: "no_sales" });
  return NextResponse.json({
    status: "ok",
    summary: toClientSummary({
      priceCents: summary.priceCents, soldAt: summary.soldAt, url: summary.url, type: summary.type,
      median30dCents: summary.median30dCents, count30d: summary.count30d, low30dCents: summary.low30dCents, high30dCents: summary.high30dCents,
    }),
  });
}
