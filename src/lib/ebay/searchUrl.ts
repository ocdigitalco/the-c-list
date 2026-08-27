/**
 * Build an eBay Partner Network (EPN) tracked search URL from DB fields — no API.
 *
 * The link drops the buyer on an eBay search for the exact card; EPN attributes
 * any resulting purchase via `campid` (the campaign) and `customid` (a per-page /
 * per-parallel sub-ID surfaced in EPN reports). The campaign id is passed in (the
 * server reads EPN_CAMPAIGN_ID and threads it to the client) so this stays a pure
 * function usable on either side.
 */
export interface EbayLinkFields {
  /** Full set label incl. year + brand + product, e.g. "2026 Topps Flagship Football". */
  setName: string;
  player: string;
  /** Subset name, or null for the set's base subset (omitted from the query). */
  subset: string | null;
  /** Parallel name; "Base" means the subset's base card (parallel omitted from query). */
  parallel: string;
  /** Print run — appended as "/<run>" for numbered parallels; omitted when null. */
  printRun: number | null;
  athleteId: number;
  setId: number;
  insertSetId: number;
  /** Parallel row id, or null for a base row. */
  parallelId: number | null;
}

const CAT_SPORTS_CARDS = "261328"; // eBay: Sports Mem, Cards & Fan Shop → Cards
const ROVER_US = "711-53200-19255-0"; // US rover (mkrid)

/** Returns the tracked search URL, or null when no campaign id is configured. */
export function buildEbaySearchUrl(f: EbayLinkFields, campaignId: string | null | undefined): string | null {
  if (!campaignId) return null;

  const parts = [f.setName, f.player];
  if (f.subset) parts.push(f.subset); // omit for the base subset (subset == null)
  if (f.parallel && f.parallel !== "Base") parts.push(f.parallel); // omit for base version
  let query = parts.filter(Boolean).join(" ").replace(/\s+/g, " ").trim();
  if (f.printRun != null) query += ` /${f.printRun}`; // numbered only

  // EPN sub-id: how conversions attribute per page/parallel in EPN reports (≤256 chars).
  const customid = `a:${f.athleteId}|s:${f.setId}|i:${f.insertSetId}|p:${f.parallelId ?? "base"}`.slice(0, 256);

  const u = new URL("https://www.ebay.com/sch/i.html");
  u.searchParams.set("_nkw", query);
  u.searchParams.set("_sacat", CAT_SPORTS_CARDS);
  u.searchParams.set("mkevt", "1");
  u.searchParams.set("mkcid", "1");
  u.searchParams.set("mkrid", ROVER_US);
  u.searchParams.set("campid", campaignId);
  u.searchParams.set("toolid", "10001");
  u.searchParams.set("customid", customid);
  return u.toString();
}
