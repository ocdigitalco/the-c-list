import { createHash } from "crypto";

// ── Config ───────────────────────────────────────────────────────────────────

// Real endpoint; overridable via env for staging / local verification (unset in prod).
export const SOLD_COMPS_ENDPOINT = process.env.SOLD_COMPS_ENDPOINT || "https://api.sold-comps.com/v1/scrape";
export const CACHE_TTL_DAYS = 14;
export const PER_IP_HOURLY_CAP = 5;
export const DEFAULT_DAILY_CAP = 150;
export const API_TIMEOUT_MS = 10_000;
/** Terms appended to every keyword to cut lots / reprints / digital / breaks. */
export const KEYWORD_EXCLUSIONS = "-lot -reprint -digital -break";

export function dailyCap(): number {
  const raw = process.env.SOLD_COMPS_DAILY_CAP;
  const n = raw ? parseInt(raw, 10) : NaN;
  return Number.isFinite(n) && n > 0 ? n : DEFAULT_DAILY_CAP;
}

// ── Pure helpers ─────────────────────────────────────────────────────────────

/**
 * "{set name} {player name} {card_number} -lot -reprint -digital -break".
 * Set name is used verbatim (its stored year prefix is part of the query).
 */
export function buildKeyword(setName: string, playerName: string, cardNumber: string): string {
  const base = `${setName} ${playerName} ${cardNumber}`.replace(/\s+/g, " ").trim();
  return `${base} ${KEYWORD_EXCLUSIONS}`;
}

export type SaleType = "auction" | "bin" | "best_offer" | null;

/**
 * Map a sold item to our stored sale type. A Best Offer acceptance wins even
 * though `soldPrice` already carries the accepted amount (hydrateBoa), so a
 * Best Offer sale stays identifiable in last_sold_type.
 */
export function mapSaleType(item: { bestOfferAccepted?: boolean | null; buyingFormat?: string | null }): SaleType {
  if (item.bestOfferAccepted === true) return "best_offer";
  switch (item.buyingFormat) {
    case "auction": return "auction";
    case "buyItNow":
    case "auctionWithBIN": return "bin";
    default: return null;
  }
}

/** Salted SHA-256 of a client IP. Raw IP is never returned or stored. */
export function hashIp(ip: string): string {
  const salt = process.env.SOLD_COMPS_IP_SALT ?? process.env.CRON_SECRET ?? "sold-comps";
  return createHash("sha256").update(`${salt}:${ip}`).digest("hex");
}

/** Best-effort client IP from proxy headers; "unknown" when none present. */
export function clientIpFrom(headers: Headers): string {
  const xff = headers.get("x-forwarded-for");
  if (xff) return xff.split(",")[0]!.trim();
  return headers.get("x-real-ip")?.trim() || "unknown";
}

function priceToCents(soldPrice: string | null | undefined): number | null {
  if (soldPrice == null) return null;
  const n = parseFloat(soldPrice);
  if (!Number.isFinite(n)) return null;
  return Math.round(n * 100);
}

function median(cents: number[]): number | null {
  if (cents.length === 0) return null;
  const s = [...cents].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 === 1 ? s[mid]! : Math.round((s[mid - 1]! + s[mid]!) / 2);
}

export interface SoldItem {
  url?: string | null;
  endedAt?: string | null; // YYYY-MM-DD
  soldPrice?: string | null; // dollars, decimal string
  buyingFormat?: string | null;
  bestOfferAccepted?: boolean | null;
}

export interface SoldSummary {
  priceCents: number;
  soldAt: string | null;
  url: string | null;
  type: SaleType;
  median30dCents: number | null;
  count30d: number;
  low30dCents: number | null;
  high30dCents: number | null;
}

/**
 * Reduce an items array to a summary: most-recent sale (by endedAt) plus 30-day
 * median/count/low/high. `now` is injected so the window is testable/deterministic.
 * Returns null when no item carries both a price and a sold date.
 */
export function summarizeItems(items: SoldItem[], now: Date): SoldSummary | null {
  const priced = items
    .map((it) => ({ it, cents: priceToCents(it.soldPrice), endedAt: it.endedAt ?? null }))
    .filter((x): x is { it: SoldItem; cents: number; endedAt: string } => x.cents != null && !!x.endedAt);
  if (priced.length === 0) return null;

  // Most recent by sold date (YYYY-MM-DD sorts lexicographically).
  const latest = priced.reduce((a, b) => (b.endedAt > a.endedAt ? b : a));

  const cutoff = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
  const within = priced.filter((x) => x.endedAt >= cutoff).map((x) => x.cents);

  return {
    priceCents: latest.cents,
    soldAt: latest.endedAt,
    url: latest.it.url ?? null,
    type: mapSaleType(latest.it),
    median30dCents: median(within),
    count30d: within.length,
    low30dCents: within.length ? Math.min(...within) : null,
    high30dCents: within.length ? Math.max(...within) : null,
  };
}

/** Collect X-Usage-* / X-Credit-* / X-RateLimit-* response headers as a plain object. */
export function collectUsageHeaders(headers: Headers): Record<string, string> {
  const out: Record<string, string> = {};
  headers.forEach((v, k) => {
    const lk = k.toLowerCase();
    if (lk.startsWith("x-usage-") || lk.startsWith("x-credit-") || lk.startsWith("x-ratelimit-")) out[k] = v;
  });
  return out;
}
