"use client";

import { useRouter } from "next/navigation";

export function SportFilter({
  sports,
  current,
  path,
  extraParams = {},
}: {
  sports: string[];
  current: string | null;
  path: string;
  extraParams?: Record<string, string>;
}) {
  const router = useRouter();

  function navigate(sport: string | null) {
    const params = new URLSearchParams(extraParams);
    if (sport) params.set("sport", sport);
    const qs = params.toString();
    router.push(qs ? `${path}?${qs}` : path);
  }

  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-0.5 [scrollbar-width:none] [-webkit-overflow-scrolling:touch]">
      <button
        onClick={() => navigate(null)}
        className={`shrink-0 px-3 py-1.5 rounded-full border text-sm font-medium transition-colors ${
          current === null
            ? "border-[var(--brand-ink)] bg-[var(--brand-ink)] text-[var(--brand-head)]"
            : "border-[var(--brand-line)] bg-[var(--brand-card)] text-[var(--brand-ink-soft)] hover:border-[var(--brand-slate)]"
        }`}
      >
        All Sports
      </button>
      {sports.map((sport) => (
        <button
          key={sport}
          onClick={() => navigate(sport)}
          className={`shrink-0 px-3 py-1.5 rounded-full border text-sm font-medium transition-colors ${
            current === sport
              ? "border-[var(--brand-ink)] bg-[var(--brand-ink)] text-[var(--brand-head)]"
              : "border-[var(--brand-line)] bg-[var(--brand-card)] text-[var(--brand-ink-soft)] hover:border-[var(--brand-slate)]"
          }`}
        >
          {sport}
        </button>
      ))}
    </div>
  );
}
