/**
 * Orchestration + read model for live eBay break spots (break_listings /
 * break_refresh_state). Uses @/lib/db, so it targets Turso in production and the
 * local file DB in dev. Written by the cron and the on-demand /api/breaks path.
 *
 * A "break" is one SELLER's active matched spot listings for a set — eBay exposes
 * no break end-time or spot totals, so seller grouping (not a time window) is the
 * only reliable unit. See ./ebay.ts for why.
 */
import { rawQuery } from "@/lib/db";
import { searchBreakListings, breaksFallbackSearchUrl } from "./ebay";

export const WHATNOT_INVITE_URL = "https://www.whatnot.com/invite/checklist2";
const DISCLOSURE = "Checklist² may earn a commission.";
// Offers/breaks stay visible across the cron cadence; on-demand refresh kicks in
// past this age so a set page never shows very stale breaks.
export const STALE_HOURS = 6;

/** True when a set's breaks are missing or older than STALE_HOURS. */
export function isStale(lastFetchedAt: string | null | undefined): boolean {
  if (!lastFetchedAt) return true;
  return (Date.now() - Date.parse(lastFetchedAt)) / 3_600_000 >= STALE_HOURS;
}

export interface RefreshSet { setId: number; slug: string; setName: string; }

const nowIso = () => new Date().toISOString();

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

/** YYYY-MM-DD cutoff = 18 months before today (matches the sealed-box window). */
function windowCutoff(): string {
  const d = new Date();
  d.setMonth(d.getMonth() - 18);
  return d.toISOString().slice(0, 10);
}

/**
 * Sets whose breaks the cron should refresh: released within 18 months (or no
 * release date). One entry per set (breaks are per-set, not per-format).
 */
export async function getBreakRefreshSets(opts: { slug?: string; limitSets?: number } = {}): Promise<RefreshSet[]> {
  const rows = await rawQuery.all<{ id: number; name: string; slug: string | null; release_date: string | null }>(
    `SELECT id, name, slug, release_date FROM sets${opts.slug ? " WHERE slug = ?" : ""} ORDER BY id`,
    ...(opts.slug ? [opts.slug] : [])
  );
  const cutoff = windowCutoff();
  const out: RefreshSet[] = [];
  for (const r of rows) {
    const inWindow = opts.slug ? true : (r.release_date == null || r.release_date === "" || r.release_date >= cutoff);
    if (!inWindow) continue;
    out.push({ setId: r.id, slug: r.slug ?? String(r.id), setName: r.name });
    if (opts.limitSets != null && out.length >= opts.limitSets) break;
  }
  return out;
}

/** Order sets by refresh staleness: never-fetched first, then oldest first. */
export async function sortSetsByFetchedAt(sets: RefreshSet[]): Promise<RefreshSet[]> {
  const rows = await rawQuery.all<{ set_id: number; last_fetched_at: string | null }>(
    "SELECT set_id, last_fetched_at FROM break_refresh_state"
  );
  const m = new Map<number, string | null>();
  for (const r of rows) m.set(r.set_id, r.last_fetched_at);
  return [...sets].sort((a, b) => {
    const fa = m.get(a.setId) ?? null;
    const fb = m.get(b.setId) ?? null;
    if (fa === fb) return a.setId - b.setId;
    if (fa === null) return -1;
    if (fb === null) return 1;
    return fa < fb ? -1 : 1;
  });
}

async function setPlayers(setId: number): Promise<{ id: number; name: string }[]> {
  return rawQuery.all<{ id: number; name: string }>("SELECT id, name FROM players WHERE set_id = ?", setId);
}

/**
 * Refresh one set's break listings. Replaces the set's rows with the current
 * matched spots (delete-then-insert) and stamps break_refresh_state. On error,
 * the existing listings are KEPT and only the error is recorded.
 */
export async function refreshSetBreaks(set: RefreshSet, opts: { timeoutMs?: number } = {}): Promise<{ ok: boolean; count: number; error?: string }> {
  try {
    const players = await setPlayers(set.setId);
    const { resultCount, listings } = await searchBreakListings({
      setName: set.setName, slug: set.slug, players, timeoutMs: opts.timeoutMs,
    });
    const fetchedAt = nowIso();
    // Preserve first_seen_at for items we already had.
    const prior = await rawQuery.all<{ item_id: string; first_seen_at: string | null }>(
      "SELECT item_id, first_seen_at FROM break_listings WHERE set_id = ?", set.setId
    );
    const firstSeen = new Map(prior.map((r) => [r.item_id, r.first_seen_at]));
    await rawQuery.run("DELETE FROM break_listings WHERE set_id = ?", set.setId);
    for (const l of listings) {
      await rawQuery.run(
        `INSERT INTO break_listings
           (source, set_id, item_id, seller, seller_feedback_pct, title, price_cents, currency,
            buying_option, format_guess, matched_player_ids, item_url, item_web_url, image_url,
            listed_at, first_seen_at, fetched_at, active)
         VALUES ('ebay', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)`,
        set.setId, l.itemId, l.seller, l.sellerFeedbackPct, l.title, l.priceCents, l.currency,
        l.buyingOption, l.formatGuess, JSON.stringify(l.matchedPlayerIds), l.itemUrl, l.itemWebUrl,
        l.imageUrl, l.listedAt, firstSeen.get(l.itemId) ?? fetchedAt, fetchedAt
      );
    }
    await rawQuery.run(
      `INSERT INTO break_refresh_state (set_id, last_fetched_at, last_result_count, last_error)
       VALUES (?, ?, ?, NULL)
       ON CONFLICT(set_id) DO UPDATE SET last_fetched_at=excluded.last_fetched_at, last_result_count=excluded.last_result_count, last_error=NULL`,
      set.setId, fetchedAt, resultCount
    );
    return { ok: true, count: listings.length };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    await rawQuery.run(
      `INSERT INTO break_refresh_state (set_id, last_fetched_at, last_result_count, last_error)
       VALUES (?, NULL, 0, ?)
       ON CONFLICT(set_id) DO UPDATE SET last_error=excluded.last_error`,
      set.setId, msg.slice(0, 500)
    );
    return { ok: false, count: 0, error: msg };
  }
}

export const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/** Time-budgeted walk of sets, refreshing break listings until budget elapses. */
export async function refreshBreaksWithinBudget(
  sets: RefreshSet[],
  opts: { budgetMs?: number; gapMs?: number; perCallTimeoutMs?: number } = {}
): Promise<{ refreshed: number; errors: number; remaining: number; processed: number; durationMs: number; refreshedSlugs: string[] }> {
  const budgetMs = opts.budgetMs ?? 25_000;
  const gapMs = opts.gapMs ?? 100;
  const start = Date.now();
  let refreshed = 0, errors = 0, processed = 0;
  const slugs = new Set<string>();
  for (let i = 0; i < sets.length; i++) {
    if (Date.now() - start >= budgetMs) break;
    const r = await refreshSetBreaks(sets[i], { timeoutMs: opts.perCallTimeoutMs ?? 8000 });
    processed++;
    if (r.ok) { refreshed++; slugs.add(sets[i].slug); } else errors++;
    if (i < sets.length - 1 && Date.now() - start < budgetMs) await sleep(gapMs);
  }
  return { refreshed, errors, remaining: sets.length - processed, processed, durationMs: Date.now() - start, refreshedSlugs: [...slugs] };
}

// ── Read model ────────────────────────────────────────────────────────────────
export interface Break {
  seller: string;
  sellerFeedbackPct: number | null;
  spotCount: number;
  startingPriceCents: number | null;
  currency: string;
  formatGuess: string | null;
  buyingLabel: string;
  listedAt: string | null;
  listedToday: boolean;
  viewUrl: string | null;
  imageUrl: string | null;
  namesPlayer: boolean; // athlete mode: a spot in this group names the player
}
export interface BreaksPayload {
  enabled: boolean;
  setSlug: string;
  setName: string;
  breaks: Break[];
  searchUrl: string | null;
  refreshedRelative: string | null;
  disclosure: string;
  whatnotUrl: string;
  playerName: string | null;
}

interface Row {
  item_id: string; seller: string | null; seller_feedback_pct: number | null;
  price_cents: number | null; currency: string | null; buying_option: string | null;
  format_guess: string | null; matched_player_ids: string | null; item_url: string | null;
  item_web_url: string | null; image_url: string | null; listed_at: string | null;
}

function buyingLabel(options: Set<string>): string {
  const hasFixed = options.has("FIXED_PRICE");
  const hasOffer = options.has("BEST_OFFER");
  const hasAuction = options.has("AUCTION");
  if (hasAuction && !hasFixed) return "Auction";
  if (hasFixed && hasOffer) return "Buy now or Best Offer";
  if (hasFixed) return "Buy now";
  if (hasOffer) return "Best Offer";
  return "Buy now";
}

function isToday(iso: string | null): boolean {
  if (!iso) return false;
  return iso.slice(0, 10) === new Date().toISOString().slice(0, 10);
}

/**
 * Build the grouped break payload for a set. When `playerId` is given (athlete
 * mode), groups whose listings name the player are flagged and sorted first, but
 * all of the set's breaks are returned — most spots are team breaks that name no
 * player, so breaking the set is itself how you pull that player.
 */
export async function getBreaksForSet(opts: {
  setId: number; setSlug: string; setName: string; playerId?: number; playerName?: string | null; max?: number;
}): Promise<BreaksPayload> {
  const campaignId = process.env.EPN_CAMPAIGN_ID ?? null;
  const base: BreaksPayload = {
    enabled: true, setSlug: opts.setSlug, setName: opts.setName, breaks: [],
    searchUrl: breaksFallbackSearchUrl(opts.setName, opts.setSlug, campaignId),
    refreshedRelative: null, disclosure: DISCLOSURE, whatnotUrl: WHATNOT_INVITE_URL,
    playerName: opts.playerName ?? null,
  };

  const rows = await rawQuery.all<Row>(
    `SELECT item_id, seller, seller_feedback_pct, price_cents, currency, buying_option,
            format_guess, matched_player_ids, item_url, item_web_url, image_url, listed_at
     FROM break_listings WHERE set_id = ? AND active = 1`,
    opts.setId
  );
  const state = await rawQuery.get<{ last_fetched_at: string | null }>(
    "SELECT last_fetched_at FROM break_refresh_state WHERE set_id = ?", opts.setId
  );
  base.refreshedRelative = state?.last_fetched_at ? relativeTime(state.last_fetched_at) : null;
  if (rows.length === 0) return base;

  // Group by seller.
  const groups = new Map<string, Row[]>();
  for (const r of rows) {
    const key = r.seller ?? "";
    if (!key) continue;
    let g = groups.get(key);
    if (!g) { g = []; groups.set(key, g); }
    g.push(r);
  }

  const breaks: Break[] = [];
  for (const [seller, list] of groups) {
    list.sort((a, b) => (a.price_cents ?? Infinity) - (b.price_cents ?? Infinity));
    const hero = list[0];
    const prices = list.map((r) => r.price_cents).filter((p): p is number => p != null);
    // Majority format guess.
    const fmtCounts = new Map<string, number>();
    for (const r of list) if (r.format_guess) fmtCounts.set(r.format_guess, (fmtCounts.get(r.format_guess) ?? 0) + 1);
    let formatGuess: string | null = null, best = 0;
    for (const [f, c] of fmtCounts) if (c > best) { best = c; formatGuess = f; }
    // Buying options union.
    const opts2 = new Set<string>();
    for (const r of list) r.buying_option?.split(",").forEach((o) => o && opts2.add(o.trim()));
    // Most-recent listed time.
    const listedAt = list.map((r) => r.listed_at).filter(Boolean).sort().slice(-1)[0] ?? null;
    // Athlete mode: does any spot name the player?
    let namesPlayer = false;
    if (opts.playerId != null) {
      for (const r of list) {
        try {
          const ids = r.matched_player_ids ? (JSON.parse(r.matched_player_ids) as number[]) : [];
          if (ids.includes(opts.playerId)) { namesPlayer = true; break; }
        } catch { /* ignore */ }
      }
    }
    breaks.push({
      seller,
      sellerFeedbackPct: hero.seller_feedback_pct,
      spotCount: list.length,
      startingPriceCents: prices.length ? Math.min(...prices) : null,
      currency: hero.currency ?? "USD",
      formatGuess,
      buyingLabel: buyingLabel(opts2),
      listedAt,
      listedToday: isToday(listedAt),
      viewUrl: hero.item_url || hero.item_web_url,
      imageUrl: hero.image_url,
      namesPlayer,
    });
  }

  breaks.sort((a, b) => {
    if (opts.playerId != null && a.namesPlayer !== b.namesPlayer) return a.namesPlayer ? -1 : 1;
    if (b.spotCount !== a.spotCount) return b.spotCount - a.spotCount;
    return (a.startingPriceCents ?? Infinity) - (b.startingPriceCents ?? Infinity);
  });

  base.breaks = breaks.slice(0, opts.max ?? 12);
  return base;
}
