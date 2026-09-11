/**
 * Orchestration for refreshing eBay sealed-box offers into ebay_box_offers.
 * Shared by the cron route and the manual refresh script. Uses @/lib/db, so it
 * targets Turso in production and the local file DB in dev (empty TURSO env).
 */
import { rawQuery } from "./db";
import { getAppToken, searchBoxOffers, normalizeFormatKey, boxFallbackSearchUrl, FORMAT_SPECS, type BoxOffer } from "./ebayBrowse";

export interface RefreshPair { setId: number; slug: string; setName: string; format: string; }

/** YYYY-MM-DD cutoff = 18 months before today. */
function windowCutoff(): string {
  const d = new Date();
  d.setMonth(d.getMonth() - 18);
  return d.toISOString().slice(0, 10);
}

/**
 * (set, format) pairs to refresh. Cron: sets released within 18 months or with
 * NULL release date. A slug narrows to one set (ignoring the window). Only
 * recognized box formats are included; keys are normalized (e.g. "Hobby"→hobby).
 */
export async function getRefreshPairs(opts: { slug?: string; limitSets?: number } = {}): Promise<{ pairs: RefreshPair[]; setsInWindow: number; setsSkippedOld: number }> {
  const rows = await rawQuery.all<{ id: number; name: string; slug: string | null; release_date: string | null; box_config: string | null }>(
    `SELECT id, name, slug, release_date, box_config FROM sets WHERE box_config IS NOT NULL AND box_config != ''${opts.slug ? " AND slug = ?" : ""} ORDER BY id`,
    ...(opts.slug ? [opts.slug] : [])
  );
  const cutoff = windowCutoff();
  const pairs: RefreshPair[] = [];
  let setsInWindow = 0, setsSkippedOld = 0;
  let usedSets = 0;
  for (const r of rows) {
    const inWindow = opts.slug ? true : (r.release_date == null || r.release_date === "" || r.release_date >= cutoff);
    if (!inWindow) { setsSkippedOld++; continue; }
    let cfg: Record<string, unknown>;
    try { cfg = JSON.parse(r.box_config!); } catch { continue; }
    if (!cfg || typeof cfg !== "object") continue;
    const fmts = Object.keys(cfg).filter((k) => cfg[k] && typeof cfg[k] === "object" && normalizeFormatKey(k));
    if (fmts.length === 0) continue;
    if (opts.limitSets != null && usedSets >= opts.limitSets) break;
    setsInWindow++; usedSets++;
    const slug = r.slug ?? String(r.id);
    // Dedupe by normalized format key (e.g. a set with both "Hobby" and "hobby").
    const seen = new Set<string>();
    for (const k of fmts) {
      const nk = normalizeFormatKey(k)!;
      if (seen.has(nk)) continue;
      seen.add(nk);
      pairs.push({ setId: r.id, slug, setName: r.name, format: nk });
    }
  }
  return { pairs, setsInWindow, setsSkippedOld };
}

const nowIso = () => new Date().toISOString();

// ── Read side: build the set-page card data ──────────────────────────────────
export interface SealedBoxFormatData { format: string; label: string; offers: BoxOffer[]; fallbackUrl: string | null; refreshedRelative: string | null; }
export interface SealedBoxData { formats: SealedBoxFormatData[]; disclosure: string; }
const FOOTER_DISCLOSURE = "Checklist² may earn a commission.";
// Two 45s cron runs clear ~146 of 168 pairs/day (eBay latency ~0.5s/call caps a
// run at ~73), so a pair refreshes every ~28h on average. 36h (not 24h) keeps
// offers visible across that cadence; tighten with a third cron window to restore 24h.
const STALE_HOURS = 36;

function relativeTime(iso: string): string {
  const diff = Date.now() - Date.parse(iso);
  const m = Math.round(diff / 60000);
  if (m < 1) return "just now";
  if (m < 60) return `${m} minute${m === 1 ? "" : "s"} ago`;
  const h = Math.round(m / 60);
  if (h < 24) return `${h} hour${h === 1 ? "" : "s"} ago`;
  const d = Math.round(h / 24);
  return `${d} day${d === 1 ? "" : "s"} ago`;
}

/**
 * Build the SealedBoxOffers card data for a set from its box_config + cached
 * offers. Offers older than 24 h (or empty) fall back to the tagged search link.
 * Returns null when the set has no recognized box formats (card hidden).
 */
export async function getSealedBoxData(setId: number, setName: string, slug: string, boxConfig: string | null): Promise<SealedBoxData | null> {
  if (!boxConfig) return null;
  let cfg: Record<string, unknown>;
  try { cfg = JSON.parse(boxConfig); } catch { return null; }
  if (!cfg || typeof cfg !== "object") return null;
  const ordered: string[] = [];
  const seen = new Set<string>();
  for (const k of Object.keys(cfg)) {
    if (!cfg[k] || typeof cfg[k] !== "object") continue;
    const nk = normalizeFormatKey(k);
    if (!nk || seen.has(nk)) continue;
    seen.add(nk); ordered.push(nk);
  }
  if (ordered.length === 0) return null;

  const rows = await rawQuery.all<{ format: string; fetched_at: string | null; offers: string | null }>(
    "SELECT format, fetched_at, offers FROM ebay_box_offers WHERE set_id = ?", setId
  );
  const byFmt = new Map(rows.map((r) => [r.format, r]));
  const campaignId = process.env.EPN_CAMPAIGN_ID ?? null;

  const formats: SealedBoxFormatData[] = [];
  for (const nk of ordered) {
    const spec = FORMAT_SPECS[nk];
    const row = byFmt.get(nk);
    let offers: BoxOffer[] = [];
    let refreshedRelative: string | null = null;
    if (row?.fetched_at && row.offers) {
      const ageH = (Date.now() - Date.parse(row.fetched_at)) / 3_600_000;
      if (ageH < STALE_HOURS) {
        try {
          const o = JSON.parse(row.offers);
          if (Array.isArray(o) && o.length > 0) { offers = o.slice(0, 3); refreshedRelative = relativeTime(row.fetched_at); }
        } catch { /* ignore */ }
      }
    }
    formats.push({
      format: nk,
      label: spec.label,
      offers,
      fallbackUrl: offers.length ? null : boxFallbackSearchUrl(setName, slug, nk, campaignId),
      refreshedRelative,
    });
  }
  if (formats.every((f) => f.offers.length === 0 && !f.fallbackUrl)) return null;
  return { formats, disclosure: FOOTER_DISCLOSURE };
}

/** Refresh one pair; upsert. On error, write `error` and KEEP the last good offers. */
export async function refreshPair(pair: RefreshPair, token: string, queryOverride?: string): Promise<{ ok: boolean; resultCount: number; best: BoxOffer | null; error?: string }> {
  try {
    const { query, resultCount, offers } = await searchBoxOffers({ token, setName: pair.setName, slug: pair.slug, formatKey: pair.format, queryOverride });
    await rawQuery.run(
      `INSERT INTO ebay_box_offers (set_id, format, query, fetched_at, offers, result_count, error)
       VALUES (?, ?, ?, ?, ?, ?, NULL)
       ON CONFLICT(set_id, format) DO UPDATE SET query=excluded.query, fetched_at=excluded.fetched_at, offers=excluded.offers, result_count=excluded.result_count, error=NULL`,
      pair.setId, pair.format, query, nowIso(), JSON.stringify(offers), resultCount
    );
    return { ok: true, resultCount, best: offers[0] ?? null };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    // Keep last good offers/fetched_at; only record the error (and the attempted query).
    await rawQuery.run(
      `INSERT INTO ebay_box_offers (set_id, format, query, fetched_at, offers, result_count, error)
       VALUES (?, ?, ?, NULL, NULL, 0, ?)
       ON CONFLICT(set_id, format) DO UPDATE SET error=excluded.error, query=excluded.query`,
      pair.setId, pair.format, queryOverride ?? "", msg.slice(0, 500)
    );
    return { ok: false, resultCount: 0, best: null, error: msg };
  }
}

export const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/**
 * Order pairs by cache staleness: never-fetched (no row) first, then oldest
 * `fetched_at` first (ISO strings sort lexicographically), stable by set/format.
 */
export async function sortPairsByFetchedAt(pairs: RefreshPair[]): Promise<RefreshPair[]> {
  const rows = await rawQuery.all<{ set_id: number; format: string; fetched_at: string | null }>(
    "SELECT set_id, format, fetched_at FROM ebay_box_offers"
  );
  const m = new Map<string, string | null>();
  for (const r of rows) m.set(`${r.set_id}||${r.format}`, r.fetched_at);
  return [...pairs].sort((a, b) => {
    const fa = m.get(`${a.setId}||${a.format}`) ?? null;
    const fb = m.get(`${b.setId}||${b.format}`) ?? null;
    if (fa === fb) return a.setId - b.setId || a.format.localeCompare(b.format);
    if (fa === null) return -1;
    if (fb === null) return 1;
    return fa < fb ? -1 : 1;
  });
}

/**
 * Walk pairs sequentially (250 ms gap) until `budgetMs` of wall time elapses,
 * then stop. Returns how many were refreshed/errored and how many remain
 * unprocessed this run. maxDuration on the route must exceed budgetMs.
 */
export async function refreshWithinBudget(
  pairs: RefreshPair[],
  opts: { budgetMs?: number; gapMs?: number } = {}
): Promise<{ refreshed: number; errors: number; remaining: number; processed: number; durationMs: number }> {
  const budgetMs = opts.budgetMs ?? 45_000;
  const gapMs = opts.gapMs ?? 100;
  const start = Date.now();
  const token = await getAppToken();
  let refreshed = 0, errors = 0, processed = 0;
  for (let i = 0; i < pairs.length; i++) {
    if (Date.now() - start >= budgetMs) break;
    const r = await refreshPair(pairs[i], token);
    processed++;
    if (r.ok) refreshed++; else errors++;
    if (i < pairs.length - 1 && Date.now() - start < budgetMs) await sleep(gapMs);
  }
  return { refreshed, errors, remaining: pairs.length - processed, processed, durationMs: Date.now() - start };
}
