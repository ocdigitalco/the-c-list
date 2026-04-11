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
        style={{
          padding: "5px 12px",
          borderRadius: 4,
          fontSize: 12,
          fontWeight: 600,
          textDecoration: "none",
          transition: "background 0.15s, color 0.15s",
          background: !activeTag ? "#1A1A1A" : "transparent",
          color: !activeTag ? "#FFFFFF" : "#6B6B6B",
          border: !activeTag ? "none" : "1px solid #E5E5E5",
        }}
      >
        All
      </Link>
      {tags.map((tag) => (
        <Link
          key={tag}
          href={`/articles?tag=${encodeURIComponent(tag)}`}
          style={{
            padding: "5px 12px",
            borderRadius: 4,
            fontSize: 12,
            fontWeight: 600,
            textDecoration: "none",
            transition: "background 0.15s, color 0.15s",
            background: activeTag === tag ? "#1A1A1A" : "transparent",
            color: activeTag === tag ? "#FFFFFF" : "#6B6B6B",
            border: activeTag === tag ? "none" : "1px solid #E5E5E5",
          }}
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
