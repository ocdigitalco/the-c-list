import { SITE_URL } from "@/lib/setSeo";
import { STATIC_SITEMAP_PATHS, athleteChunkPaths, xmlEscape } from "@/lib/athletes/sitemap";

// A single sitemap child. `/sitemaps/0.xml` = static routes; `/sitemaps/N.xml` =
// athlete chunk N (≤10,000 URLs). Cached, not per-request dynamic.
export const revalidate = 86400;

export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const chunk = parseInt(id.replace(/\.xml$/, ""), 10);
  if (!Number.isFinite(chunk) || chunk < 0) {
    return new Response("Not found", { status: 404 });
  }

  const now = new Date().toISOString();
  let entries: { path: string; freq: string }[];
  if (chunk === 0) {
    entries = STATIC_SITEMAP_PATHS.map((p) => ({ path: p, freq: "daily" }));
  } else {
    const paths = await athleteChunkPaths(chunk);
    entries = paths.map((p) => ({ path: p, freq: "weekly" }));
  }

  const body =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    entries
      .map(
        (e) =>
          `  <url><loc>${xmlEscape(`${SITE_URL}${e.path}`)}</loc><lastmod>${now}</lastmod><changefreq>${e.freq}</changefreq></url>`
      )
      .join("\n") +
    `\n</urlset>\n`;

  return new Response(body, {
    headers: {
      "Content-Type": "application/xml",
      "Cache-Control": "public, s-maxage=86400, stale-while-revalidate=86400",
    },
  });
}
