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

// Theme tags are neutral: --track fill, --soft text, --line border (no per-tag hues).
const NEUTRAL_TAG = "bg-[var(--brand-track)] text-[var(--brand-ink-soft)] border border-[var(--brand-line)]";
const TAG_STYLES: Record<string, string> = {
  checklist:    NEUTRAL_TAG,
  "box-config": NEUTRAL_TAG,
  odds:         NEUTRAL_TAG,
  feature:      NEUTRAL_TAG,
  announcement: NEUTRAL_TAG,
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
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium capitalize ${TAG_STYLES[tag] ?? "bg-[var(--brand-track)] text-[var(--brand-ink-soft)]"}`}>
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
                ? "bg-[var(--brand-ink)] text-[var(--brand-head)] font-medium"
                : "bg-[var(--brand-card)] text-[var(--brand-ink-soft)] border border-[var(--brand-line)] hover:border-[var(--brand-line)] hover:text-[var(--brand-ink)]"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Feed */}
      {filtered.length === 0 ? (
        <p className="text-sm text-[var(--brand-slate)]">No updates for this filter.</p>
      ) : (
        <div className="space-y-px">
          {filtered.map((update, i) => {
            const prevDate = i > 0 ? filtered[i - 1].date.slice(0, 10) : null;
            const thisDate = update.date.slice(0, 10);
            const showDateDivider = prevDate !== thisDate;

            return (
              <div key={update.id}>
                {showDateDivider && i > 0 && (
                  <div className="h-px bg-[var(--brand-track)] my-6" />
                )}
                <div className="group rounded-xl border border-[var(--brand-line)] bg-[var(--brand-card)] px-6 py-5 hover:border-[var(--brand-line)] hover:bg-[var(--brand-card)] transition-colors mb-3">
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mb-2">
                        <time className="text-xs text-[var(--brand-slate)] shrink-0" dateTime={update.date}>
                          {formatDate(update.date)}
                        </time>
                        <div className="flex flex-wrap gap-1.5">
                          {update.tags.map((tag) => (
                            <TagBadge key={tag} tag={tag} />
                          ))}
                        </div>
                      </div>
                      <h2 className="text-base font-semibold text-[var(--brand-ink)] mb-1.5 leading-snug">
                        {update.title}
                      </h2>
                      <p className="text-sm text-[var(--brand-ink-soft)] leading-relaxed">
                        {update.summary}
                      </p>
                    </div>
                    <Link
                      href={`/updates/${update.id}`}
                      className="shrink-0 text-sm text-[var(--brand-slate)] group-hover:text-[var(--brand-ink-soft)] transition-colors whitespace-nowrap"
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
