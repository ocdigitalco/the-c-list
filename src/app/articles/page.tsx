import type { Metadata } from "next";
import Link from "next/link";
import { articles, getAllTags } from "@/lib/articles";
import { PageShell } from "@/components/PageShell";
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

  return (
    <PageShell
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="Articles"
      description="Guides, insights, and how-tos for collectors and breakers"
    >
        {/* Tag filter */}
        <ArticleTagFilter tags={allTags} current={activeTag ?? null} />

        {/* Article cards */}
        {filtered.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {filtered.map((article) => (
              <Link
                key={article.id}
                href={`/articles/${article.id}`}
                className="group block rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden hover:border-zinc-600 hover:bg-zinc-800/60 transition-colors"
              >
                {/* Hero thumbnail */}
                <div className="aspect-[16/9] bg-zinc-800 overflow-hidden">
                  {article.heroImage && !article.heroImage.includes("placeholder") ? (
                    <img
                      src={article.heroImage}
                      alt={article.title}
                      className="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-300"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <svg
                        className="w-10 h-10 text-zinc-700"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={1.5}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z"
                        />
                      </svg>
                    </div>
                  )}
                </div>

                {/* Card body */}
                <div className="px-5 py-4 space-y-3">
                  <h2 className="text-base font-semibold text-white leading-snug group-hover:text-amber-400 transition-colors">
                    {article.title}
                  </h2>
                  <p className="text-sm text-zinc-400 leading-relaxed line-clamp-2">
                    {article.description}
                  </p>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-1.5">
                    {article.tags.slice(0, 4).map((tag) => (
                      <span
                        key={tag}
                        className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-400 border border-zinc-700"
                      >
                        {tag}
                      </span>
                    ))}
                    {article.tags.length > 4 && (
                      <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-500">
                        +{article.tags.length - 4}
                      </span>
                    )}
                  </div>

                  {/* Date + Read more */}
                  <div className="flex items-center justify-between pt-1">
                    <time className="text-xs text-zinc-600">{formatDate(article.publishedAt)}</time>
                    <span className="text-xs font-medium text-zinc-500 group-hover:text-amber-400 transition-colors">
                      Read more &rarr;
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <p className="text-sm text-zinc-500">No articles found for this tag.</p>
          </div>
        )}
    </PageShell>
  );
}
