/**
 * eBay Browse API client for live sealed-box listings, with EPN affiliate
 * tagging applied by eBay (via X-EBAY-C-ENDUSERCTX). Server-only — reads
 * EBAY_CLIENT_ID / EBAY_CLIENT_SECRET (OAuth) and EPN_CAMPAIGN_ID (campid).
 *
 * The app OAuth token is cached in-memory for (expires_in - 60)s.
 */

const OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token";
const SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search";
const MARKETPLACE = "EBAY_US";

// Negative keywords appended to every query AND used to drop stray titles.
export const NEGATIVE_KEYWORDS = [
  "break", "breaks", "spot", "spots", "repack", "repacks",
  "empty", "lot", "pack", "packs", "single", "singles",
];
const NEGATIVE_QUERY = NEGATIVE_KEYWORDS.map((w) => `-${w}`).join(" ");

// Recognized box_config format keys → { display label, query phrase (incl. "box"),
// price floor }. Unrecognized formats are skipped by the cron. Keys are matched
// case-insensitively (so "Hobby" folds into "hobby").
export interface FormatSpec { label: string; phrase: string; floor: number; }
export const FORMAT_SPECS: Record<string, FormatSpec> = {
  hobby: { label: "Hobby", phrase: "hobby box", floor: 40 },
  jumbo: { label: "Jumbo", phrase: "jumbo box", floor: 40 },
  mega: { label: "Mega", phrase: "mega box", floor: 25 },
  blaster: { label: "Blaster", phrase: "blaster box", floor: 10 },
  value: { label: "Value", phrase: "value box", floor: 10 },
  hanger: { label: "Hanger", phrase: "hanger box", floor: 10 },
  fdi: { label: "First Day Issue", phrase: "first day issue box", floor: 40 },
  first_day_issue: { label: "First Day Issue", phrase: "first day issue box", floor: 40 },
  value_blaster: { label: "Value Blaster", phrase: "value blaster box", floor: 10 },
  breaker: { label: "Breaker", phrase: "breaker box", floor: 40 },
  mania: { label: "Mania", phrase: "mania box", floor: 10 },
  // Ruling additions (2026-09 go):
  breakers_delight: { label: "Breaker's Delight", phrase: "breaker's delight box", floor: 40 },
  hobby_jumbo: { label: "Hobby Jumbo", phrase: "jumbo box", floor: 40 },
  sapphire: { label: "Sapphire", phrase: "sapphire box", floor: 100 },
};

export function normalizeFormatKey(key: string): string | null {
  const k = key.trim().toLowerCase();
  return k in FORMAT_SPECS ? k : null;
}

/** Strip ®/™ and parentheticals from a set name, collapse whitespace. */
function cleanName(name: string): string {
  return name.replace(/[®™]/g, "").replace(/\([^)]*\)/g, "").replace(/\s+/g, " ").trim();
}

/** Split a set name into leading year token (e.g. "2026" or "2025-26") + rest. */
function splitYear(name: string): { year: string; rest: string } {
  const m = name.match(/\b(19|20)\d{2}(-\d{2})?\b/);
  if (!m) return { year: "", rest: name };
  const year = m[0];
  const rest = name.replace(year, "").replace(/\s+/g, " ").trim();
  return { year, rest };
}

/** Keyword query for a (set, format): "<year> <name-no-year> <phrase> <negatives>". */
export function boxSearchQuery(setName: string, formatKey: string): string {
  const spec = FORMAT_SPECS[normalizeFormatKey(formatKey) ?? ""];
  const phrase = spec ? spec.phrase : "box";
  const { year, rest } = splitYear(cleanName(setName));
  const q = [year, rest, phrase].filter(Boolean).join(" ");
  return `${q} ${NEGATIVE_QUERY}`.replace(/\s+/g, " ").trim();
}

/** Tagged eBay keyword-search URL (no API) for the "no offers" fallback. */
export function boxFallbackSearchUrl(setName: string, slug: string, formatKey: string, campaignId: string | null | undefined): string | null {
  if (!campaignId) return null;
  const { year, rest } = splitYear(cleanName(setName));
  const spec = FORMAT_SPECS[normalizeFormatKey(formatKey) ?? ""];
  const nkw = [year, rest, spec ? spec.phrase : "box"].filter(Boolean).join(" ");
  const u = new URL("https://www.ebay.com/sch/i.html");
  u.searchParams.set("_nkw", nkw);
  u.searchParams.set("LH_BIN", "1"); // Buy It Now
  u.searchParams.set("LH_ItemCondition", "1000"); // New
  u.searchParams.set("mkevt", "1");
  u.searchParams.set("mkcid", "1");
  u.searchParams.set("mkrid", "711-53200-19255-0");
  u.searchParams.set("campid", campaignId);
  u.searchParams.set("toolid", "10001");
  u.searchParams.set("customid", slug.slice(0, 256));
  return u.toString();
}

// ── Offer type ───────────────────────────────────────────────────────────────
export interface BoxOffer {
  itemId: string;
  title: string;
  price: number;
  shipping: number;
  total: number;
  currency: string;
  url: string;
  imageUrl: string | null;
  seller: string | null;
  sellerFeedbackPct: number | null;
  condition: string | null;
  shippingUnknown: boolean;
}

// ── Token cache ────────────────────────────────────────────────────────────────
let cachedToken: { token: string; exp: number } | null = null;

export async function getAppToken(): Promise<string> {
  const now = Date.now();
  if (cachedToken && cachedToken.exp > now) return cachedToken.token;
  const id = process.env.EBAY_CLIENT_ID, secret = process.env.EBAY_CLIENT_SECRET;
  if (!id || !secret) throw new Error("EBAY_CLIENT_ID / EBAY_CLIENT_SECRET not set");
  const basic = Buffer.from(`${id}:${secret}`).toString("base64");
  const res = await fetch(OAUTH_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded", Authorization: `Basic ${basic}` },
    body: "grant_type=client_credentials&scope=https%3A%2F%2Fapi.ebay.com%2Foauth%2Fapi_scope",
  });
  if (!res.ok) throw new Error(`eBay OAuth failed: ${res.status} ${await res.text().catch(() => "")}`);
  const data = (await res.json()) as { access_token?: string; expires_in?: number };
  if (!data.access_token) throw new Error("eBay OAuth: no access_token");
  cachedToken = { token: data.access_token, exp: now + (Math.max(0, (data.expires_in ?? 7200) - 60)) * 1000 };
  return cachedToken.token;
}

/** For tests: force the next getAppToken() to refetch (e.g. bad-token simulation). */
export function _clearTokenCache() { cachedToken = null; }

// ── Search + filter/rank ─────────────────────────────────────────────────────
interface EbayItem {
  itemId?: string; title?: string;
  price?: { value?: string; currency?: string };
  shippingOptions?: { shippingCost?: { value?: string; currency?: string } }[];
  itemWebUrl?: string; itemAffiliateWebUrl?: string;
  image?: { imageUrl?: string }; thumbnailImages?: { imageUrl?: string }[];
  seller?: { username?: string; feedbackPercentage?: string };
  condition?: string;
}

const hasNegative = (title: string) => {
  const t = title.toLowerCase();
  return NEGATIVE_KEYWORDS.some((w) => new RegExp(`\\b${w}\\b`, "i").test(t));
};

export function filterAndRank(items: EbayItem[]): BoxOffer[] {
  const offers: BoxOffer[] = [];
  for (const it of items) {
    const title = (it.title ?? "").trim();
    if (!title) continue;
    if (!/\bbox\b/i.test(title)) continue;       // must be a box
    if (hasNegative(title)) continue;             // belt & braces vs stray listings
    const price = parseFloat(it.price?.value ?? "");
    if (!isFinite(price)) continue;
    const so = it.shippingOptions?.[0]?.shippingCost?.value;
    const shipping = so != null ? parseFloat(so) : NaN;
    const shippingUnknown = !isFinite(shipping);
    const ship = shippingUnknown ? 0 : shipping;
    offers.push({
      itemId: it.itemId ?? "",
      title,
      price,
      shipping: ship,
      total: price + ship,
      currency: it.price?.currency ?? "USD",
      url: it.itemAffiliateWebUrl || it.itemWebUrl || "",
      imageUrl: it.image?.imageUrl ?? it.thumbnailImages?.[0]?.imageUrl ?? null,
      seller: it.seller?.username ?? null,
      sellerFeedbackPct: it.seller?.feedbackPercentage != null ? parseFloat(it.seller.feedbackPercentage) : null,
      condition: it.condition ?? null,
      shippingUnknown,
    });
  }
  offers.sort((a, b) => a.total - b.total);
  return offers.slice(0, 3);
}

export interface SearchResult { query: string; resultCount: number; offers: BoxOffer[]; }

/** Run one (set, format) search. `queryOverride` is for the nonsense-query gate. */
export async function searchBoxOffers(opts: {
  token: string; setName: string; slug: string; formatKey: string; queryOverride?: string;
}): Promise<SearchResult> {
  const spec = FORMAT_SPECS[normalizeFormatKey(opts.formatKey) ?? ""];
  const floor = spec ? spec.floor : 10;
  const query = opts.queryOverride ?? boxSearchQuery(opts.setName, opts.formatKey);
  const campaignId = process.env.EPN_CAMPAIGN_ID ?? "";
  const url = new URL(SEARCH_URL);
  url.searchParams.set("q", query);
  url.searchParams.set("filter", `conditions:{NEW},buyingOptions:{FIXED_PRICE},itemLocationCountry:US,priceCurrency:USD,price:[${floor}..]`);
  url.searchParams.set("sort", "price");
  url.searchParams.set("limit", "25");
  const res = await fetch(url.toString(), {
    headers: {
      Authorization: `Bearer ${opts.token}`,
      "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE,
      "X-EBAY-C-ENDUSERCTX": `affiliateCampaignId=${campaignId},affiliateReferenceId=${opts.slug}`,
    },
  });
  if (!res.ok) throw new Error(`eBay search ${res.status}: ${(await res.text().catch(() => "")).slice(0, 300)}`);
  const data = (await res.json()) as { itemSummaries?: EbayItem[]; total?: number };
  const items = data.itemSummaries ?? [];
  return { query, resultCount: data.total ?? items.length, offers: filterAndRank(items) };
}
