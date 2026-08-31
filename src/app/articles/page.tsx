import type { Metadata } from "next";
import Link from "next/link";
import { articles, getAllTags, type Article } from "@/lib/articles";
import { Footer } from "@/components/Footer";
import { ArticleTagFilter } from "./ArticleTagFilter";

export const metadata: Metadata = {
  title: "Articles — Checklist2",
  description: "Guides, insights, and how-tos for collectors and breakers",
};

function estimateReadTime(a: Article): string {
  const bodyWords = a.content
    .filter((s) => s.type === "p" || s.type === "h2" || s.type === "h3")
    .reduce((sum, s) => sum + (s.text?.split(/\s+/).length ?? 0), 0);
  const mins = Math.max(3, Math.ceil(bodyWords / 200));
  return `${mins} MIN READ`;
}

function categoryTag(a: Article): string | null {
  if (!a.tags || a.tags.length === 0) return null;
  return a.tags[0].toUpperCase();
}

// ─── Hero Article (position 1) ──────────────────────────────────────────────

function HeroArticle({ article: a }: { article: Article }) {
  const cat = categoryTag(a);
  return (
    <Link href={`/articles/${a.id}`} className="group block" style={{ textDecoration: "none" }}>
      <div style={{ background: "#F5F5F5" }}>
        {a.heroImage && !a.heroImage.includes("placeholder") ? (
          <img src={a.heroImage} alt={a.title} width={800} height={500} loading="eager"
            className="w-full transition-transform duration-500 group-hover:scale-[1.02]"
            style={{ display: "block", aspectRatio: "16/10", objectFit: "cover" }} />
        ) : (
          <div className="flex items-center justify-center"
            style={{ background: "#2C2C2A", aspectRatio: "16/10" }}>
            <span style={{ color: "#6B6B6B", fontSize: 18, fontWeight: 700 }}>Checklist{"\u00b2"}</span>
          </div>
        )}
      </div>
      <div style={{ paddingTop: 16 }}>
        {cat && (
          <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", color: "var(--brand-accent)", display: "block", marginBottom: 6 }}>
            {cat}
          </span>
        )}
        <h2 className="group-hover:underline" style={{
          fontSize: 28, fontWeight: 700, lineHeight: 1.22, color: "#1A1A1A", margin: "0 0 8px 0",
          fontFamily: "Georgia, 'Times New Roman', serif",
        }}>
          {a.title}
        </h2>
        <span style={{ fontSize: 11, fontWeight: 600, letterSpacing: "0.06em", color: "#999999" }}>
          {estimateReadTime(a)}
        </span>
      </div>
    </Link>
  );
}

// ─── Featured Sidebar Article (position 2) ──────────────────────────────────

function FeaturedSidebarArticle({ article: a }: { article: Article }) {
  return (
    <Link href={`/articles/${a.id}`} className="group block" style={{ textDecoration: "none" }}>
      {a.heroImage && !a.heroImage.includes("placeholder") ? (
        <div style={{ overflow: "hidden", marginBottom: 14, aspectRatio: "16/10" }}>
          <img src={a.heroImage} alt={a.title} width={400} height={250} loading="eager"
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.03]"
            style={{ display: "block" }} />
        </div>
      ) : (
        <div className="flex items-center justify-center"
          style={{ background: "#2C2C2A", aspectRatio: "16/10", marginBottom: 14 }}>
          <span style={{ color: "#6B6B6B", fontSize: 14, fontWeight: 700 }}>Checklist{"\u00b2"}</span>
        </div>
      )}
      <h3 className="group-hover:underline" style={{
        fontSize: 18, fontWeight: 700, lineHeight: 1.3, color: "#1A1A1A", margin: "0 0 8px 0",
        fontFamily: "Georgia, 'Times New Roman', serif",
      }}>
        {a.title}
      </h3>
      <span style={{ fontSize: 11, fontWeight: 600, letterSpacing: "0.06em", color: "#999999" }}>
        {estimateReadTime(a)}
      </span>
    </Link>
  );
}

// ─── Sidebar Article (positions 3-4) ────────────────────────────────────────

function SidebarArticle({ article: a }: { article: Article }) {
  return (
    <Link href={`/articles/${a.id}`} className="group flex items-start gap-4" style={{ textDecoration: "none" }}>
      <div style={{ flex: 1, minWidth: 0 }}>
        <h3 className="group-hover:underline" style={{
          fontSize: 16, fontWeight: 700, lineHeight: 1.3, color: "#1A1A1A", margin: "0 0 6px 0",
          fontFamily: "Georgia, 'Times New Roman', serif",
          display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical" as const, overflow: "hidden",
        }}>
          {a.title}
        </h3>
        <span style={{ fontSize: 11, fontWeight: 600, letterSpacing: "0.06em", color: "#999999" }}>
          {estimateReadTime(a)}
        </span>
      </div>
      {a.heroImage && !a.heroImage.includes("placeholder") && (
        <div className="shrink-0" style={{ width: 100, height: 100, overflow: "hidden" }}>
          <img src={a.heroImage} alt={a.title} width={100} height={100} loading="lazy"
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.03]" />
        </div>
      )}
    </Link>
  );
}

// ─── Compact Article (positions 5-8) ────────────────────────────────────────

function CompactArticle({ article: a }: { article: Article }) {
  const cat = categoryTag(a);
  return (
    <Link href={`/articles/${a.id}`} className="group block" style={{ textDecoration: "none" }}>
      {cat && (
        <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: "0.1em", color: "var(--brand-accent)", display: "block", marginBottom: 4 }}>
          {cat}
        </span>
      )}
      <span style={{ fontSize: 10, fontWeight: 600, letterSpacing: "0.06em", color: "#999999", display: "block", marginBottom: 8 }}>
        {estimateReadTime(a)}
      </span>
      <h3 className="group-hover:underline" style={{
        fontSize: 18, fontWeight: 700, lineHeight: 1.3, color: "#1A1A1A", margin: 0,
        fontFamily: "Georgia, 'Times New Roman', serif",
      }}>
        {a.title}
      </h3>
    </Link>
  );
}

// ─── Page ───────────────────────────────────────────────────────────────────

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

  const hero = filtered[0] ?? null;
  const featuredSidebar = filtered[1] ?? null;
  const compactSidebar = filtered.slice(2, 4);
  const compactRow = filtered.slice(4, 8);
  const remainder = filtered.slice(8);

  return (
    <div className="h-full overflow-y-auto" style={{ background: "var(--brand-card)" }}>
      <div className="page-container">
        {/* Header */}
        <div style={{ paddingTop: 40, paddingBottom: 12, borderBottom: "1px solid var(--brand-line)" }}>
          <h1 style={{ fontSize: 13, fontWeight: 700, letterSpacing: "0.12em", textTransform: "uppercase" as const, color: "#1A1A1A", margin: 0 }}>
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
            {/* ── Hero + Sidebar ── */}
            {hero && (
              <section className="flex flex-col lg:flex-row" style={{ gap: 0 }}>
                {/* Hero (left 2/3) */}
                <div className="lg:flex-[65] lg:border-r" style={{ borderColor: "var(--brand-line)" }}>
                  <div className="lg:mr-6">
                    <HeroArticle article={hero} />
                  </div>
                </div>

                {/* Sidebar (right 1/3) */}
                {featuredSidebar && (
                  <aside className="lg:flex-[35] lg:pl-6 pt-6 lg:pt-0">
                    <div className="flex flex-col">
                      {/* Position 2: Featured (image on top) */}
                      <div style={{
                        paddingBottom: 16,
                        marginBottom: compactSidebar.length > 0 ? 16 : 0,
                        borderBottom: compactSidebar.length > 0 ? "1px solid var(--brand-line)" : "none",
                      }}>
                        <FeaturedSidebarArticle article={featuredSidebar} />
                      </div>
                      {/* Positions 3-4: Compact (thumbnail right) */}
                      {compactSidebar.map((a, i) => (
                        <div key={a.id} style={{
                          paddingBottom: 16,
                          marginBottom: i < compactSidebar.length - 1 ? 16 : 0,
                          borderBottom: i < compactSidebar.length - 1 ? "1px solid var(--brand-line)" : "none",
                        }}>
                          <SidebarArticle article={a} />
                        </div>
                      ))}
                    </div>
                  </aside>
                )}
              </section>
            )}

            {/* ── Compact Row (positions 5-8) ── */}
            {compactRow.length > 0 && (
              <section style={{ borderTop: "1px solid var(--brand-line)", marginTop: 32, paddingTop: 24 }}>
                <div className="grid gap-0" style={{
                  gridTemplateColumns: `repeat(${Math.min(compactRow.length, 4)}, 1fr)`,
                }}>
                  {compactRow.map((a, i) => (
                    <div key={a.id} style={{
                      padding: "0 20px",
                      borderLeft: i > 0 ? "1px solid var(--brand-line)" : "none",
                    }}>
                      <CompactArticle article={a} />
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* ── Remainder (position 9+) ── */}
            {remainder.length > 0 && (
              <section style={{ borderTop: "1px solid var(--brand-line)", marginTop: 32, paddingTop: 24 }}>
                <div className="flex flex-col">
                  {remainder.map((a) => (
                    <div key={a.id} style={{ paddingBottom: 16, marginBottom: 16, borderBottom: "1px solid var(--brand-line)" }}>
                      <SidebarArticle article={a} />
                    </div>
                  ))}
                </div>
              </section>
            )}

            <div style={{ height: 64 }} />
          </>
        )}
      </div>
      <Footer />
    </div>
  );
}
