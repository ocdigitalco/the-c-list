"use client";

import { useEffect, useRef, useState } from "react";

interface StatCardData {
  label: string;
  value: number;
  tooltip?: string;
}

function AnimatedNumber({ target }: { target: number }) {
  const [current, setCurrent] = useState(0);
  const ref = useRef<number | null>(null);

  useEffect(() => {
    const duration = 800;
    const start = performance.now();
    function tick(now: number) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setCurrent(Math.round(eased * target));
      if (progress < 1) {
        ref.current = requestAnimationFrame(tick);
      }
    }
    ref.current = requestAnimationFrame(tick);
    return () => {
      if (ref.current) cancelAnimationFrame(ref.current);
    };
  }, [target]);

  return <>{current.toLocaleString()}</>;
}

function StatCard({ label, value, tooltip }: StatCardData) {
  return (
    <div
      className="relative rounded-lg px-4 py-4 transition-shadow hover:shadow-md"
      style={{
        background: "var(--v2-card-bg)",
        border: "1px solid var(--v2-border)",
        borderLeft: "3px solid var(--v2-accent)",
        boxShadow: "var(--v2-card-shadow)",
      }}
    >
      <div className="flex items-center gap-1">
        <p
          className="text-[13px] font-medium"
          style={{ color: "var(--v2-text-secondary)" }}
        >
          {label}
        </p>
        {tooltip && (
          <span className="group relative cursor-help">
            <svg
              className="w-3.5 h-3.5 opacity-40"
              style={{ color: "var(--v2-text-secondary)" }}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
              />
            </svg>
            <span
              className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1.5 px-2 py-1 text-[10px] rounded whitespace-nowrap opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-10"
              style={{ background: "var(--v2-text-primary)", color: "var(--v2-page-bg)" }}
            >
              {tooltip}
            </span>
          </span>
        )}
      </div>
      <p
        className="text-[26px] font-bold mt-1"
        style={{ color: "var(--v2-accent)", fontVariantNumeric: "tabular-nums" }}
      >
        <AnimatedNumber target={value} />
      </p>
    </div>
  );
}

interface Props {
  cards: number;
  parallelTypes: number;
  totalParallels: number;
  insertSets: number;
  autographs: number;
  autoParallels: number;
}

export function StatCards({
  cards,
  parallelTypes,
  totalParallels,
  insertSets,
  autographs,
  autoParallels,
}: Props) {
  const items: StatCardData[] = [
    { label: "Cards", value: cards, tooltip: "Total unique cards in this set" },
    { label: "Parallel Types", value: parallelTypes, tooltip: "Count of distinct parallel names" },
    { label: "Total Parallels", value: totalParallels, tooltip: "Total parallel entries across all insert sets" },
    { label: "Insert Sets", value: insertSets, tooltip: "Distinct insert set groupings" },
    { label: "Autographs", value: autographs, tooltip: "Cards in autograph insert sets" },
    { label: "Auto Parallels", value: autoParallels, tooltip: "Parallels on autograph insert sets" },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-3 gap-3">
      {items.map((item) => (
        <StatCard key={item.label} {...item} />
      ))}
    </div>
  );
}
