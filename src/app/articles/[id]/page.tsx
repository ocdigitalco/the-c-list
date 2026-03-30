import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { articles, getArticleById, getAdjacentArticles } from "@/lib/articles";
import type { ArticleSection } from "@/lib/articles";
import { PageShell } from "@/components/PageShell";

export async function generateStaticParams() {
  return articles.map((a) => ({ id: a.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const article = getArticleById(id);
  if (!article) return {};
  return {
    title: `${article.title} — Checklist2`,
    description: article.description,
  };
}

function formatDate(iso: string) {
  return new Date(iso + "T00:00:00Z").toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

function isYouTube(url: string): string | null {
  const m =
    url.match(/youtube\.com\/watch\?v=([^&]+)/) ??
    url.match(/youtu\.be\/([^?]+)/) ??
    url.match(/youtube\.com\/embed\/([^?]+)/);
  return m ? m[1] : null;
}

function ArticleContent({ section }: { section: ArticleSection }) {
  switch (section.type) {
    case "h2":
      return (
        <h2 className="text-xl font-bold text-white tracking-tight mt-10 mb-4">
          {section.text}
        </h2>
      );
    case "h3":
      return (
        <h3 className="text-lg font-semibold text-white mt-8 mb-3">
          {section.text}
        </h3>
      );
    case "h4":
      return (
        <h4 className="text-base font-semibold text-white mt-6 mb-2">
          {section.text}
        </h4>
      );
    case "p":
      return (
        <p className="text-sm text-zinc-400 leading-relaxed mb-4">
          {section.text}
        </p>
      );
    case "ul":
      return (
        <ul className="space-y-2 mb-4">
          {section.items?.map((item, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-zinc-400 leading-relaxed">
              <span className="shrink-0 text-zinc-600 mt-0.5">&bull;</span>
              {item}
            </li>
          ))}
        </ul>
      );
    case "ol":
      return (
        <ol className="space-y-2 mb-4">
          {section.items?.map((item, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-zinc-400 leading-relaxed">
              <span className="shrink-0 text-zinc-500 font-medium tabular-nums mt-0.5 w-5 text-right">
                {i + 1}.
              </span>
              {item}
            </li>
          ))}
        </ol>
      );
    case "image":
      return (
        <figure className="mb-6">
          <img
            src={section.src}
            alt={section.alt ?? ""}
            className="w-full rounded-lg border border-zinc-800"
          />
          {section.caption && (
            <figcaption className="text-xs text-zinc-600 mt-2 text-center">
              {section.caption}
            </figcaption>
          )}
        </figure>
      );
    case "link":
      return (
        <p className="text-sm mb-4">
          <a
            href={section.href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-amber-400 hover:text-amber-300 underline underline-offset-2 transition-colors inline-flex items-center gap-1"
          >
            {section.text}
            <svg className="w-3 h-3 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
            </svg>
          </a>
        </p>
      );
    case "video": {
      const ytId = section.src ? isYouTube(section.src) : null;
      if (ytId) {
        return (
          <div className="aspect-video rounded-lg overflow-hidden border border-zinc-800 mb-6">
            <iframe
              src={`https://www.youtube.com/embed/${ytId}`}
              title={section.alt ?? "Video"}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="w-full h-full"
            />
          </div>
        );
      }
      return (
        <div className="aspect-video rounded-lg overflow-hidden border border-zinc-800 mb-6">
          <video src={section.src} controls className="w-full h-full" />
        </div>
      );
    }
    default:
      return null;
  }
}

export default async function ArticlePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const article = getArticleById(id);
  if (!article) notFound();

  const { prev, next } = getAdjacentArticles(id);

  return (
    <PageShell
      breadcrumb={{ label: "Articles", href: "/articles" }}
      title={article.title}
      description={formatDate(article.publishedAt)}
    >
        {/* Tags */}
        <div className="flex flex-wrap gap-1.5 -mt-4">
          {article.tags.map((tag) => (
            <span
              key={tag}
              className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-400 border border-zinc-700"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Hero image */}
        {article.heroImage && !article.heroImage.includes("placeholder") ? (
          <div className="rounded-xl overflow-hidden border border-zinc-800">
            <img
              src={article.heroImage}
              alt={article.title}
              className="w-full aspect-[16/9] object-cover"
            />
          </div>
        ) : (
          <div className="rounded-xl overflow-hidden border border-zinc-800 bg-zinc-800 aspect-[16/9] flex items-center justify-center">
            <svg
              className="w-16 h-16 text-zinc-700"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z"
              />
            </svg>
          </div>
        )}

        {/* TL;DR */}
        <div className="rounded-xl border border-amber-700/30 bg-amber-950/20 px-6 py-5">
          <p className="text-xs font-bold text-amber-400 uppercase tracking-widest mb-2">
            TL;DR
          </p>
          <p className="text-sm text-zinc-300 leading-relaxed">{article.tldr}</p>
        </div>

        {/* Article body */}
        <div>
          {article.content.map((section, i) => (
            <ArticleContent key={i} section={section} />
          ))}
        </div>

        {/* Prev / Next navigation */}
        {(prev || next) && (
          <div className="mt-4 pt-8 border-t border-zinc-800 grid grid-cols-2 gap-4">
            <div>
              {next && (
                <Link href={`/articles/${next.id}`} className="group block">
                  <p className="text-xs text-zinc-600 mb-1">&larr; Older</p>
                  <p className="text-sm text-zinc-400 group-hover:text-zinc-200 transition-colors leading-snug line-clamp-2">
                    {next.title}
                  </p>
                  <p className="text-xs text-zinc-600 mt-0.5">
                    {formatDate(next.publishedAt)}
                  </p>
                </Link>
              )}
            </div>
            <div className="text-right">
              {prev && (
                <Link href={`/articles/${prev.id}`} className="group block">
                  <p className="text-xs text-zinc-600 mb-1">Newer &rarr;</p>
                  <p className="text-sm text-zinc-400 group-hover:text-zinc-200 transition-colors leading-snug line-clamp-2">
                    {prev.title}
                  </p>
                  <p className="text-xs text-zinc-600 mt-0.5">
                    {formatDate(prev.publishedAt)}
                  </p>
                </Link>
              )}
            </div>
          </div>
        )}
    </PageShell>
  );
}
