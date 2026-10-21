"use client";

import { useRouter } from "next/navigation";
import styles from "./TimeRangeTabs.module.css";

// Shared segmented time-range selector used by /searches and /sheets. Range is
// expressed as the `range` query param; `params` carries any other query params
// that must survive the navigation (e.g. /searches `sport`, /sheets `secret`).
export const TIME_RANGES = [
  { label: "24h", value: "24h" },
  { label: "7 days", value: "7d" },
  { label: "30 days", value: "30d" },
  { label: "1 year", value: "1y" },
  { label: "All time", value: "all" },
] as const;

export type TimeRange = (typeof TIME_RANGES)[number]["value"];

export function TimeRangeTabs({
  current,
  basePath,
  params = {},
}: {
  current: string;
  basePath: string;
  params?: Record<string, string>;
}) {
  const router = useRouter();

  function navigate(range: string) {
    const sp = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) {
      if (v) sp.set(k, v);
    }
    sp.set("range", range);
    router.push(`${basePath}?${sp.toString()}`);
  }

  return (
    <div className={styles.seg}>
      {TIME_RANGES.map((r) => {
        const on = current === r.value;
        return (
          <button
            key={r.value}
            className={on ? `${styles.segBtn} ${styles.segOn}` : styles.segBtn}
            aria-pressed={on}
            onClick={() => navigate(r.value)}
          >
            {r.label}
          </button>
        );
      })}
    </div>
  );
}
