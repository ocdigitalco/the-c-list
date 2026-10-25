/**
 * eBay Browse API client for live BREAK-SPOT listings — the "Trading Card Box &
 * Case Breaks" category (261334). This is the inverse of ebayBrowse.ts (sealed
 * boxes): here we KEEP break spots and drop whole sealed boxes.
 *
 * Probe findings (2026-10, confirmed with fieldgroups=EXTENDED) that shape this:
 *   • Category 261334 is correct (chain 212 → 64482 → 261334).
 *   • itemAffiliateWebUrl IS returned → EPN tagging works exactly like boxes.
 *   • seller/feedback/price/buyingOptions/itemWebUrl/itemCreationDate present.
 *   • bidCount, itemEndDate, estimatedAvailableQuantity are ALL ABSENT — so no
 *     countdown, no "X/Y open spots", no auction bid counts are possible. Every
 *     spot is FIXED_PRICE (often +BEST_OFFER). We therefore group by seller only,
 *     count visible active spots, and show buyingOptions + "listed" time.
 *
 * Server-only — reuses the OAuth token from ebayBrowse.ts and EPN_CAMPAIGN_ID.
 */

import { getAppToken } from "@/lib/ebayBrowse";

const SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search";
const MARKETPLACE = "EBAY_US";

/** eBay leaf category: Sports Mem, Cards & Fan Shop › … › Box & Case Breaks. */
export const BREAKS_CATEGORY_ID = "261334";

// A listing in category 261334 is a break SPOT (not a whole sealed box/case) when
// its title carries one of these break tokens. Pure sealed-box listings mislisted
// in the category carry none and are dropped — this cleanly separates the two.
const BREAK_TOKEN_RE =
  /\b(break|breaks|breaking|pyt|pyp|pyd|ptp|random|rt|mixer|spot|spots|filler|fillers|slot|slots|division)\b|pick\s*your|break\s*#/i;

/** Strip ®/™ and parentheticals; collapse whitespace. */
function cleanName(name: string): string {
  return name.replace(/[®™]/g, "").replace(/\([^)]*\)/g, "").replace(/\s+/g, " ").trim();
}

/** Leading year token (e.g. "2026" or "2025-26"), or "" when absent. */
function yearToken(name: string): string {
  const m = name.match(/\b(19|20)\d{2}(-\d{2})?\b/);
  return m ? m[0] : "";
}

/** Keyword query for a set's breaks: "<year> <name>" (category scopes the rest). */
export function breaksSearchQuery(setName: string): string {
  return cleanName(setName);
}

/**
 * Confirm a listing title really is for THIS set: the year token must appear, and
 * at least half of the set's distinctive product tokens (min 1) must appear. Keeps
 * cross-product noise out of a category that mixes every sport/brand. The probe
 * measured ~0 false positives against this rule (878: 6/6, 896: 50/50).
 */
export function confirmSet(title: string, setName: string): boolean {
  const t = title.toLowerCase();
  const clean = cleanName(setName);
  const year = yearToken(clean);
  if (year && !t.includes(year.toLowerCase())) return false;
  const tokens = clean
    .toLowerCase()
    .replace(year.toLowerCase(), " ")
    .split(/[^a-z0-9]+/)
    .filter((w) => w.length >= 3 && w !== "the");
  if (tokens.length === 0) return !!year; // nothing to match on besides the year
  const hits = tokens.filter((w) => t.includes(w)).length;
  return hits >= Math.ceil(tokens.length / 2);
}

/** True when the title is a break spot (vs a whole sealed box/case). */
export function isBreakSpot(title: string): boolean {
  return BREAK_TOKEN_RE.test(title);
}

/** Coarse break-format guess from the title, or null for a generic break. */
export function inferFormat(title: string): string | null {
  const t = title.toLowerCase();
  if (/\bpyt\b|pick\s*your\s*team/.test(t)) return "PYT";
  if (/\bpyp\b|pick\s*your\s*player/.test(t)) return "PYP";
  if (/\bpyd\b|pick\s*your\s*(division|conference)/.test(t)) return "PYD";
  if (/\brandom\b|\brt\b/.test(t)) return "random";
  if (/case\s*break/.test(t)) return "case";
  if (/\bmixer\b/.test(t)) return "mixer";
  if (/\bteam\b/.test(t)) return "team";
  return null;
}

/** Player ids whose FULL name appears in the title (case-insensitive substring). */
export function matchPlayers(title: string, players: { id: number; name: string }[]): number[] {
  const t = title.toLowerCase();
  const ids: number[] = [];
  for (const p of players) {
    const n = p.name.toLowerCase().trim();
    if (n.length >= 4 && t.includes(n)) ids.push(p.id);
  }
  return ids;
}

// ── Parsed listing ────────────────────────────────────────────────────────────
export interface BreakListing {
  itemId: string;
  title: string;
  seller: string | null;
  sellerFeedbackPct: number | null;
  priceCents: number | null;
  currency: string;
  buyingOption: string | null; // comma-joined, e.g. "FIXED_PRICE,BEST_OFFER"
  formatGuess: string | null;
  matchedPlayerIds: number[];
  itemUrl: string | null; // affiliate when available
  itemWebUrl: string | null;
  imageUrl: string | null;
  listedAt: string | null; // itemCreationDate
}

interface EbayItem {
  itemId?: string;
  title?: string;
  price?: { value?: string; currency?: string };
  buyingOptions?: string[];
  itemWebUrl?: string;
  itemAffiliateWebUrl?: string;
  image?: { imageUrl?: string };
  thumbnailImages?: { imageUrl?: string }[];
  seller?: { username?: string; feedbackPercentage?: string };
  itemCreationDate?: string;
  categories?: { categoryId?: string }[];
}

/**
 * Fetch and classify a set's live break spots from category 261334. Confirms the
 * set, drops whole sealed boxes, infers format, and matches player names. The
 * eBay call is aborted after `timeoutMs` so an on-demand refresh can't hang.
 */
export async function searchBreakListings(opts: {
  setName: string;
  slug: string;
  players?: { id: number; name: string }[];
  limit?: number;
  timeoutMs?: number;
}): Promise<{ query: string; resultCount: number; listings: BreakListing[] }> {
  const token = await getAppToken();
  const query = breaksSearchQuery(opts.setName);
  const campaignId = process.env.EPN_CAMPAIGN_ID ?? "";
  const players = opts.players ?? [];

  const url = new URL(SEARCH_URL);
  url.searchParams.set("q", query);
  url.searchParams.set("category_ids", BREAKS_CATEGORY_ID);
  url.searchParams.set("filter", "itemLocationCountry:US,priceCurrency:USD,price:[1..]");
  url.searchParams.set("sort", "price");
  url.searchParams.set("limit", String(opts.limit ?? 50));

  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), opts.timeoutMs ?? 8000);
  let data: { itemSummaries?: EbayItem[]; total?: number };
  try {
    const res = await fetch(url.toString(), {
      signal: ctrl.signal,
      headers: {
        Authorization: `Bearer ${token}`,
        "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE,
        // affiliateReferenceId surfaces as `customid` on the returned affiliate
        // URL. Namespace break links as `breaks:<set-slug>` (the athlete page
        // appends `:<player-id>` at render time).
        "X-EBAY-C-ENDUSERCTX": `affiliateCampaignId=${campaignId},affiliateReferenceId=breaks:${opts.slug}`,
      },
    });
    if (!res.ok) throw new Error(`eBay breaks search ${res.status}: ${(await res.text().catch(() => "")).slice(0, 300)}`);
    data = (await res.json()) as { itemSummaries?: EbayItem[]; total?: number };
  } finally {
    clearTimeout(timer);
  }

  const items = data.itemSummaries ?? [];
  const listings: BreakListing[] = [];
  for (const it of items) {
    const title = (it.title ?? "").trim();
    if (!title || !it.itemId) continue;
    if (!confirmSet(title, opts.setName)) continue;
    if (!isBreakSpot(title)) continue; // drop whole sealed boxes / cases
    const price = parseFloat(it.price?.value ?? "");
    listings.push({
      itemId: it.itemId,
      title,
      seller: it.seller?.username ?? null,
      sellerFeedbackPct: it.seller?.feedbackPercentage != null ? parseFloat(it.seller.feedbackPercentage) : null,
      priceCents: isFinite(price) ? Math.round(price * 100) : null,
      currency: it.price?.currency ?? "USD",
      buyingOption: it.buyingOptions?.length ? it.buyingOptions.join(",") : null,
      formatGuess: inferFormat(title),
      matchedPlayerIds: matchPlayers(title, players),
      itemUrl: it.itemAffiliateWebUrl || it.itemWebUrl || null,
      itemWebUrl: it.itemWebUrl ?? null,
      imageUrl: it.image?.imageUrl ?? it.thumbnailImages?.[0]?.imageUrl ?? null,
      listedAt: it.itemCreationDate ?? null,
    });
  }
  return { query, resultCount: data.total ?? items.length, listings };
}

/** Tagged eBay category-search URL (no API) for the "See all breaks" / empty link. */
export function breaksFallbackSearchUrl(setName: string, slug: string, campaignId: string | null | undefined): string | null {
  if (!campaignId) return null;
  const u = new URL("https://www.ebay.com/sch/i.html");
  u.searchParams.set("_nkw", breaksSearchQuery(setName));
  u.searchParams.set("_sacat", BREAKS_CATEGORY_ID); // Box & Case Breaks category
  u.searchParams.set("mkevt", "1");
  u.searchParams.set("mkcid", "1");
  u.searchParams.set("mkrid", "711-53200-19255-0");
  u.searchParams.set("campid", campaignId);
  u.searchParams.set("toolid", "10001");
  u.searchParams.set("customid", `breaks:${slug}`.slice(0, 256));
  return u.toString();
}
