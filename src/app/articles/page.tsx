import type { Metadata } from "next";
import Link from "next/link";
import { articles, getAllTags } from "@/lib/articles";
import { Footer } from "@/components/Footer";
import { ArticleTagFilter } from "./ArticleTagFilter";

export const metadata: Metadata = {
  title: "Articles — Checklist2",
  description: "Guides, insights, and how-tos for collectors and breakers",
};

function formatDate(iso: string) {
  return new Date(iso + "T00:00:00Z").toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

function estimateReadTime(description: string): string {
  const words = description.split(/\s+/).length;
  const mins = Math.max(3, Math.ceil(words / 40));
  return `${mins} min read`;
}

export default async function ArticlesPage({
  searchParams,
}: {
  searchParams: Promise<{ tag?: string }>;
}) {
  const { tag: activeTag } = await searchParams;
  const allTags = getAllTags();
  const filtered = activeTag
    ? articles.filter((a) => a.tags.includes(activeTag))
    : articles;

  const [hero, second, ...remaining] = filtered;

  return (
    <div className="h-full overflow-y-auto" style={{ background: "#FFFFFF" }}>
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 24px" }}>
        {/* Header */}
        <div style={{ paddingTop: 40, paddingBottom: 12, borderBottom: "1px solid #E5E5E5" }}>
          <h1
            style={{
              fontSize: 13,
              fontWeight: 700,
              letterSpacing: "0.12em",
              textTransform: "uppercase" as const,
              color: "#1A1A1A",
              margin: 0,
            }}
          >
            Articles
          </h1>
        </div>

        {/* Tag filter */}
        <div style={{ padding: "12px 0 20px" }}>
          <ArticleTagFilter tags={allTags} current={activeTag ?? null} />
        </div>

        {filtered.length === 0 ? (
          <div style={{ textAlign: "center", padding: "80px 0", color: "#6B6B6B", fontSize: 14 }}>
            No articles found for this tag.
          </div>
        ) : (
          <>
            {/* Two-column layout: hero left, list right */}
            <div className="flex flex-col lg:flex-row" style={{ gap: 0 }}>
              {/* ── Left column: Hero article ── */}
              {hero && (
                <Link
                  href={`/articles/${hero.id}`}
                  className="group block lg:flex-[65] lg:border-r"
                  style={{
                    textDecoration: "none",
                    borderColor: "#E5E5E5",
                  }}
                >
                  <div className="lg:mr-6">
                    {/* Hero image */}
                    <div style={{ background: "#F5F5F5" }}>
                      {hero.heroImage && !hero.heroImage.includes("placeholder") ? (
                        <img
                          src={hero.heroImage}
                          alt={hero.title}
                          className="w-full transition-transform duration-500 group-hover:scale-[1.02]"
                          style={{ display: "block" }}
                        />
                      ) : (
                        <div
                          className="flex items-center justify-center"
                          style={{ background: "#2C2C2A", aspectRatio: "16/9" }}
                        >
                          <span style={{ color: "#6B6B6B", fontSize: 18, fontWeight: 700 }}>
                            Checklist{"\u00b2"}
                          </span>
                        </div>
                      )}
                    </div>
                    {/* Title below image */}
                    <div style={{ paddingTop: 16 }}>
                      <h2
                        className="group-hover:underline"
                        style={{
                          fontSize: 28,
                          fontWeight: 700,
                          lineHeight: 1.22,
                          color: "#1A1A1A",
                          margin: "0 0 8px 0",
                          fontFamily: "Georgia, 'Times New Roman', serif",
                        }}
                      >
                        {hero.title}
                      </h2>
                      <span
                        style={{
                          fontSize: 11,
                          fontWeight: 600,
                          letterSpacing: "0.06em",
                          textTransform: "uppercase" as const,
                          color: "#999999",
                        }}
                      >
                        {estimateReadTime(hero.description)}
                      </span>
                    </div>
                  </div>
                </Link>
              )}

              {/* ── Right column: Stacked articles ── */}
              <div className="lg:flex-[35] lg:pl-6 pt-6 lg:pt-0">
                {/* First right article — with image */}
                {second && (
                  <Link
                    href={`/articles/${second.id}`}
                    className="group block"
                    style={{
                      textDecoration: "none",
                      paddingBottom: 20,
                      borderBottom: "1px solid #E5E5E5",
                      marginBottom: 16,
                    }}
                  >
                    {second.heroImage && !second.heroImage.includes("placeholder") && (
                      <div
                        style={{
                          overflow: "hidden",
                          marginBottom: 14,
                          aspectRatio: "16/9",
                        }}
                      >
                        <img
                          src={second.heroImage}
                          alt={second.title}
                          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.03]"
                        />
                      </div>
                    )}
                    <h3
                      className="group-hover:underline"
                      style={{
                        fontSize: 18,
                        fontWeight: 700,
                        lineHeight: 1.3,
                        color: "#1A1A1A",
                        margin: "0 0 6px 0",
                        fontFamily: "Georgia, 'Times New Roman', serif",
                      }}
                    >
                      {second.title}
                    </h3>
                    <span
                      style={{
                        fontSize: 11,
                        fontWeight: 600,
                        letterSpacing: "0.06em",
                        textTransform: "uppercase" as const,
                        color: "#999999",
                      }}
                    >
                      {estimateReadTime(second.description)}
                    </span>
                  </Link>
                )}

                {/* Remaining articles — horizontal row: headline left, thumbnail right */}
                {remaining.map((article) => (
                  <Link
                    key={article.id}
                    href={`/articles/${article.id}`}
                    className="group flex items-start gap-4"
                    style={{
                      textDecoration: "none",
                      paddingBottom: 16,
                      borderBottom: "1px solid #E5E5E5",
                      marginBottom: 16,
                    }}
                  >
                    {/* Text */}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <h3
                        className="group-hover:underline"
                        style={{
                          fontSize: 16,
                          fontWeight: 700,
                          lineHeight: 1.3,
                          color: "#1A1A1A",
                          margin: "0 0 6px 0",
                          fontFamily: "Georgia, 'Times New Roman', serif",
                          display: "-webkit-box",
                          WebkitLineClamp: 3,
                          WebkitBoxOrient: "vertical" as const,
                          overflow: "hidden",
                        }}
                      >
                        {article.title}
                      </h3>
                      <span
                        style={{
                          fontSize: 11,
                          fontWeight: 600,
                          letterSpacing: "0.06em",
                          textTransform: "uppercase" as const,
                          color: "#999999",
                        }}
                      >
                        {estimateReadTime(article.description)}
                      </span>
                    </div>

                    {/* Small square thumbnail */}
                    {article.heroImage && !article.heroImage.includes("placeholder") && (
                      <div
                        className="shrink-0"
                        style={{
                          width: 100,
                          height: 100,
                          overflow: "hidden",
                        }}
                      >
                        <img
                          src={article.heroImage}
                          alt={article.title}
                          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.03]"
                        />
                      </div>
                    )}
                  </Link>
                ))}
              </div>
            </div>

            {/* Bottom spacer */}
            <div style={{ height: 64 }} />
          </>
        )}
      </div>
      <Footer />
    </div>
  );
}
