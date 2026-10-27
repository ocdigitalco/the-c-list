import { SITE_URL } from "@/lib/setSeo";
import { athleteChunkCount, xmlEscape } from "@/lib/athletes/sitemap";

// Sitemap index → one child per chunk. Chunk 0 is the static routes; chunks
// 1..N are indexed athlete URLs (≤10,000 each). Cached, not per-request dynamic.
export const revalidate = 86400;

export async function GET() {
  const chunks = await athleteChunkCount();
  const now = new Date().toISOString();
  const ids = [0];
  for (let i = 1; i <= chunks; i++) ids.push(i);

  const body =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    ids
      .map(
        (id) =>
          `  <sitemap><loc>${xmlEscape(`${SITE_URL}/sitemaps/${id}.xml`)}</loc><lastmod>${now}</lastmod></sitemap>`
      )
      .join("\n") +
    `\n</sitemapindex>\n`;

  return new Response(body, {
    headers: {
      "Content-Type": "application/xml",
      "Cache-Control": "public, s-maxage=86400, stale-while-revalidate=86400",
    },
  });
}
