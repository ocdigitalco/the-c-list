import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { updates, getUpdateById, getAdjacentUpdates } from "@/lib/updates";
import { MarkdownContent } from "@/components/MarkdownContent";
import { PageShell } from "@/components/PageShell";

const TAG_STYLES: Record<string, string> = {
  checklist:    "bg-blue-950 text-blue-300 border border-blue-700/50",
  "box-config": "bg-amber-950 text-amber-300 border border-amber-700/50",
  odds:         "bg-violet-950 text-violet-300 border border-violet-700/50",
  feature:      "bg-emerald-950 text-emerald-300 border border-emerald-700/50",
  announcement: "bg-rose-950 text-rose-300 border border-rose-700/50",
};

function TagBadge({ tag }: { tag: string }) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${TAG_STYLES[tag] ?? "bg-zinc-800 text-zinc-300"}`}>
      {tag === "box-config" ? "Box Config" : tag.charAt(0).toUpperCase() + tag.slice(1)}
    </span>
  );
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

function formatDateTime(iso: string) {
  return new Date(iso).toLocaleString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
    timeZoneName: "short",
    timeZone: "UTC",
  });
}

export async function generateStaticParams() {
  return updates.map((u) => ({ id: u.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params;
  const update = getUpdateById(id);
  if (!update) return {};
  return {
    title: `${update.title} — Checklist2`,
    description: update.summary,
  };
}

export default async function UpdatePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const update = getUpdateById(id);
  if (!update) notFound();

  const { prev, next } = getAdjacentUpdates(id);

  return (
    <PageShell
      breadcrumb={{ label: "Updates", href: "/updates" }}
      title={update.title}
      description={formatDate(update.date)}
    >
        <div className="flex flex-wrap gap-1.5">
          {update.tags.map((tag) => (
            <TagBadge key={tag} tag={tag} />
          ))}
        </div>

        <p className="text-base text-zinc-400 leading-relaxed">
          {update.summary}
        </p>

        {update.setId && (
          <Link
            href={`/sets/${update.setId}`}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-zinc-800 text-sm font-medium text-zinc-300 hover:bg-zinc-700 hover:text-white transition-colors"
          >
            &rarr; View Checklist
          </Link>
        )}

        {/* Divider */}
        <div className="h-px bg-zinc-800" />

        {/* Body */}
        <div className="prose-sm">
          <MarkdownContent content={update.description} />
        </div>

        {/* Prev / Next navigation */}
        <div className="mt-4 pt-8 border-t border-zinc-800 grid grid-cols-2 gap-4">
          <div>
            {next && (
              <Link
                href={`/updates/${next.id}`}
                className="group block"
              >
                <p className="text-xs text-zinc-600 mb-1">&larr; Older</p>
                <p className="text-sm text-zinc-400 group-hover:text-zinc-200 transition-colors leading-snug line-clamp-2">
                  {next.title}
                </p>
                <p className="text-xs text-zinc-600 mt-0.5">{formatDate(next.date)}</p>
              </Link>
            )}
          </div>
          <div className="text-right">
            {prev && (
              <Link
                href={`/updates/${prev.id}`}
                className="group block"
              >
                <p className="text-xs text-zinc-600 mb-1">Newer &rarr;</p>
                <p className="text-sm text-zinc-400 group-hover:text-zinc-200 transition-colors leading-snug line-clamp-2">
                  {prev.title}
                </p>
                <p className="text-xs text-zinc-600 mt-0.5">{formatDate(prev.date)}</p>
              </Link>
            )}
          </div>
        </div>
    </PageShell>
  );
}
