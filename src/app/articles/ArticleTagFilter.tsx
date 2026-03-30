"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

function TagFilterInner({ tags, current }: { tags: string[]; current: string | null }) {
  const searchParams = useSearchParams();
  const activeTag = current ?? searchParams.get("tag");

  return (
    <div className="flex flex-wrap gap-1.5">
      <Link
        href="/articles"
        className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
          !activeTag
            ? "bg-zinc-700 text-white"
            : "text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/60"
        }`}
      >
        All
      </Link>
      {tags.map((tag) => (
        <Link
          key={tag}
          href={`/articles?tag=${encodeURIComponent(tag)}`}
          className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
            activeTag === tag
              ? "bg-zinc-700 text-white"
              : "text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/60"
          }`}
        >
          {tag}
        </Link>
      ))}
    </div>
  );
}

export function ArticleTagFilter({ tags, current }: { tags: string[]; current: string | null }) {
  return (
    <Suspense fallback={null}>
      <TagFilterInner tags={tags} current={current} />
    </Suspense>
  );
}
