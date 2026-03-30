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
        className={`shrink-0 px-3 py-1.5 rounded-lg border text-sm font-medium transition-colors ${
          current === null
            ? "border-amber-500/60 bg-amber-500/10 text-amber-400"
            : "border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-600 hover:text-zinc-200"
        }`}
      >
        All Sports
      </button>
      {sports.map((sport) => (
        <button
          key={sport}
          onClick={() => navigate(sport)}
          className={`shrink-0 px-3 py-1.5 rounded-lg border text-sm font-medium transition-colors ${
            current === sport
              ? "border-amber-500/60 bg-amber-500/10 text-amber-400"
              : "border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-600 hover:text-zinc-200"
          }`}
        >
          {sport}
        </button>
      ))}
    </div>
  );
}
