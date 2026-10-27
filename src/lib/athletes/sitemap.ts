import { rawQuery } from "@/lib/db";

// Shared sitemap data for the index + chunk route handlers.
// Chunk 0 = static top-level routes; chunks 1..N = indexed athlete URLs, ≤10,000
// each. A thin athlete page (card_count < 3 AND set_count = 1) is noindex and
// excluded; page_kind = 'none' has no page at all.
export const SITEMAP_CHUNK = 10000;

const INDEXED_WHERE = `page_kind != 'none' AND NOT (card_count < 3 AND set_count = 1)`;

export const STATIC_SITEMAP_PATHS = [
  "/",
  "/checklists",
  "/sets",
  "/athletes",
  "/overview",
  "/searches",
  "/resources",
  "/articles",
  "/updates",
];

const KIND_SEG: Record<string, string | null> = {
  player: "athletes",
  character: "characters",
  person: "people",
  team: "teams",
  none: null,
};

export async function indexedAthleteCount(): Promise<number> {
  try {
    const row = await rawQuery.get<{ n: number }>(`SELECT COUNT(*) AS n FROM athletes WHERE ${INDEXED_WHERE}`);
    return row?.n ?? 0;
  } catch {
    return 0;
  }
}

/** Number of athlete chunks (at least 0). Index has chunk 0 (statics) + these. */
export async function athleteChunkCount(): Promise<number> {
  const n = await indexedAthleteCount();
  return Math.ceil(n / SITEMAP_CHUNK);
}

/** Relative athlete paths for chunk index `c` (1-based; chunk 0 is statics). */
export async function athleteChunkPaths(c: number): Promise<string[]> {
  if (c < 1) return [];
  let rows: { slug: string; page_kind: string }[] = [];
  try {
    rows = await rawQuery.all<{ slug: string; page_kind: string }>(
      `SELECT slug, page_kind FROM athletes WHERE ${INDEXED_WHERE} ORDER BY id LIMIT ? OFFSET ?`,
      SITEMAP_CHUNK,
      (c - 1) * SITEMAP_CHUNK
    );
  } catch {
    return [];
  }
  return rows
    .map((r) => {
      const seg = KIND_SEG[r.page_kind];
      return seg ? `/${seg}/${r.slug}` : null;
    })
    .filter((p): p is string => p != null);
}

export function xmlEscape(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
