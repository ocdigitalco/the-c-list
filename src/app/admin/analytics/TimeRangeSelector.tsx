"use client";

import { useRouter } from "next/navigation";

const RANGES = [
  { label: "24h", value: "24h" },
  { label: "7 days", value: "7d" },
  { label: "30 days", value: "30d" },
  { label: "1 year", value: "1y" },
  { label: "All time", value: "all" },
] as const;

export function TimeRangeSelector({ current, sport }: { current: string; sport: string | null }) {
  const router = useRouter();

  function navigate(range: string) {
    const params = new URLSearchParams();
    params.set("range", range);
    if (sport) params.set("sport", sport);
    router.push(`/admin/analytics?${params.toString()}`);
  }

  return (
    <div className="flex items-center gap-1 bg-zinc-900 border border-zinc-800 rounded-lg p-1">
      {RANGES.map((r) => (
        <button
          key={r.value}
          onClick={() => navigate(r.value)}
          className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
            current === r.value
              ? "bg-zinc-700 text-white"
              : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800"
          }`}
        >
          {r.label}
        </button>
      ))}
    </div>
  );
}
