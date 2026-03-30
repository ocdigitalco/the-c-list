"use client";

import { useState } from "react";
import Link from "next/link";
import type { Update } from "@/lib/updates";

const ALL_TAGS = [
  { value: "all", label: "All" },
  { value: "checklist", label: "Checklist" },
  { value: "box-config", label: "Box Config" },
  { value: "odds", label: "Odds" },
  { value: "feature", label: "Feature" },
  { value: "announcement", label: "Announcement" },
];

const TAG_STYLES: Record<string, string> = {
  checklist:    "bg-blue-950 text-blue-300 border border-blue-700/50",
  "box-config": "bg-amber-950 text-amber-300 border border-amber-700/50",
  odds:         "bg-violet-950 text-violet-300 border border-violet-700/50",
  feature:      "bg-emerald-950 text-emerald-300 border border-emerald-700/50",
  announcement: "bg-rose-950 text-rose-300 border border-rose-700/50",
};

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

function TagBadge({ tag }: { tag: string }) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium capitalize ${TAG_STYLES[tag] ?? "bg-zinc-800 text-zinc-300"}`}>
      {tag === "box-config" ? "Box Config" : tag.charAt(0).toUpperCase() + tag.slice(1)}
    </span>
  );
}

export function UpdatesFeed({ updates }: { updates: Update[] }) {
  const [activeTag, setActiveTag] = useState("all");

  const filtered = activeTag === "all"
    ? updates
    : updates.filter((u) => u.tags.includes(activeTag));

  return (
    <div>
      {/* Filter bar */}
      <div className="flex flex-wrap gap-2 mb-8">
        {ALL_TAGS.map((t) => (
          <button
            key={t.value}
            onClick={() => setActiveTag(t.value)}
            className={`px-3 py-1.5 rounded-md text-sm transition-colors ${
              activeTag === t.value
                ? "bg-zinc-700 text-white font-medium"
                : "bg-zinc-900 text-zinc-400 border border-zinc-800 hover:border-zinc-600 hover:text-zinc-200"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Feed */}
      {filtered.length === 0 ? (
        <p className="text-sm text-zinc-500">No updates for this filter.</p>
      ) : (
        <div className="space-y-px">
          {filtered.map((update, i) => {
            const prevDate = i > 0 ? filtered[i - 1].date.slice(0, 10) : null;
            const thisDate = update.date.slice(0, 10);
            const showDateDivider = prevDate !== thisDate;

            return (
              <div key={update.id}>
                {showDateDivider && i > 0 && (
                  <div className="h-px bg-zinc-800/60 my-6" />
                )}
                <div className="group rounded-xl border border-zinc-800 bg-zinc-900/60 px-6 py-5 hover:border-zinc-700 hover:bg-zinc-900 transition-colors mb-3">
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mb-2">
                        <time className="text-xs text-zinc-500 shrink-0" dateTime={update.date}>
                          {formatDate(update.date)}
                        </time>
                        <div className="flex flex-wrap gap-1.5">
                          {update.tags.map((tag) => (
                            <TagBadge key={tag} tag={tag} />
                          ))}
                        </div>
                      </div>
                      <h2 className="text-base font-semibold text-white mb-1.5 leading-snug">
                        {update.title}
                      </h2>
                      <p className="text-sm text-zinc-400 leading-relaxed">
                        {update.summary}
                      </p>
                    </div>
                    <Link
                      href={`/updates/${update.id}`}
                      className="shrink-0 text-sm text-zinc-500 group-hover:text-zinc-300 transition-colors whitespace-nowrap"
                    >
                      Read more →
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
