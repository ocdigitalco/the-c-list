"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { MonogramTile } from "./MonogramTile";
import { athleteHref, isRecentRookie } from "@/lib/athletes/util";
import type { AthleteTile, AthleteSort } from "@/lib/athletes/queries";

const FONT_DISPLAY = "var(--cl-font-display), var(--brand-font-head), system-ui, sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

const SORT_OPTIONS: { value: AthleteSort; label: string }[] = [
  { value: "cards", label: "Most cards" },
  { value: "trending", label: "Trending" },
  { value: "az", label: "A–Z" },
  { value: "newest", label: "Newest sets" },
];

export function AthletesIndexClient({
  initialTiles,
  initialTotal,
  initialHasMore,
  sports,
  totalAll,
}: {
  initialTiles: AthleteTile[];
  initialTotal: number;
  initialHasMore: boolean;
  sports: string[];
  totalAll: number;
}) {
  const [sport, setSport] = useState("All");
  const [q, setQ] = useState("");
  const [rookie, setRookie] = useState(false);
  const [sort, setSort] = useState<AthleteSort>("cards");

  const [tiles, setTiles] = useState<AthleteTile[]>(initialTiles);
  const [total, setTotal] = useState(initialTotal);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(initialHasMore);
  const [loading, setLoading] = useState(false);

  // A default view (no filters) is the server-rendered first page; skip the
  // initial fetch so it paints instantly.
  const isDefault = sport === "All" && q.trim() === "" && !rookie && sort === "cards";
  const didMount = useRef(false);
  const reqId = useRef(0);

  const fetchPage = useCallback(
    async (nextPage: number, append: boolean) => {
      const id = ++reqId.current;
      setLoading(true);
      const params = new URLSearchParams();
      if (sport !== "All") params.set("sport", sport);
      if (q.trim()) params.set("q", q.trim());
      if (rookie) params.set("rookie", "1");
      if (sort !== "cards") params.set("sort", sort);
      params.set("page", String(nextPage));
      try {
        const res = await fetch(`/api/athletes?${params.toString()}`);
        const data = await res.json();
        if (id !== reqId.current) return; // a newer request superseded this one
        setTiles((prev) => (append ? [...prev, ...data.tiles] : data.tiles));
        setTotal(data.total);
        setPage(data.page);
        setHasMore(data.hasMore);
      } finally {
        if (id === reqId.current) setLoading(false);
      }
    },
    [sport, q, rookie, sort]
  );

  // Refetch page 0 whenever a filter changes (debounced for the query box).
  useEffect(() => {
    if (!didMount.current) {
      didMount.current = true;
      return;
    }
    if (isDefault) {
      setTiles(initialTiles);
      setTotal(initialTotal);
      setPage(0);
      setHasMore(initialHasMore);
      return;
    }
    const t = setTimeout(() => fetchPage(0, false), q.trim() ? 250 : 0);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sport, q, rookie, sort]);

  const countLabel = `${(isDefault ? totalAll : total).toLocaleString()} ATHLETES`;

  const chipBase: React.CSSProperties = {
    border: 0,
    cursor: "pointer",
    fontSize: 14.5,
    padding: "10px 16px",
    borderRadius: 999,
    background: "transparent",
    color: "var(--brand-ink)",
  };

  return (
    <main style={{ width: "100%", maxWidth: 1330, margin: "0 auto", padding: "44px 16px 80px", boxSizing: "border-box", display: "flex", flexDirection: "column", gap: 28 }}>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <Link href="/" style={{ fontSize: 13, color: "var(--brand-slate)" }}>
          ‹ Home
        </Link>
        <h1 className="page-title" style={{ margin: 0, fontSize: 48, lineHeight: 1.05, letterSpacing: "-0.01em" }}>
          Athletes
        </h1>
        <p style={{ margin: 0, fontSize: 15, color: "var(--brand-slate)" }}>
          Every player, character, and creator across every set — find one to see all their cards.
        </p>
      </div>

      {/* Sport chips */}
      <div style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" }}>
        <span style={{ font: `500 11px ${FONT_MONO}`, letterSpacing: "0.14em", color: "var(--brand-slate)", marginRight: 12 }}>
          SPORT
        </span>
        {["All", ...sports].map((s) => {
          const active = s === sport;
          return (
            <button
              key={s}
              onClick={() => setSport(s)}
              aria-pressed={active}
              style={{
                ...chipBase,
                background: active ? "var(--brand-ink)" : "transparent",
                color: active ? "#fff" : "var(--brand-ink)",
                border: active ? 0 : "1px solid var(--brand-line)",
              }}
            >
              {s}
            </button>
          );
        })}
      </div>

      {/* Search + rookie toggle + sort */}
      <div style={{ display: "flex", gap: 12, alignItems: "stretch", flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 260, display: "flex", alignItems: "center", gap: 12, background: "var(--brand-track)", borderRadius: 8, padding: "0 18px", height: 48, border: "1px solid var(--brand-line)" }}>
          <span aria-hidden style={{ width: 12, height: 12, border: "1.5px solid var(--brand-slate)", borderRadius: "50%", flex: "none" }} />
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search by athlete, team, or league…"
            aria-label="Search athletes"
            style={{ flex: 1, border: 0, background: "transparent", fontSize: 15, outline: "none", color: "var(--brand-ink)" }}
          />
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, background: "var(--brand-track)", borderRadius: 8, padding: "0 6px", border: "1px solid var(--brand-line)" }}>
          <button
            onClick={() => setRookie((r) => !r)}
            aria-pressed={rookie}
            style={{ border: 0, cursor: "pointer", fontSize: 13.5, padding: "9px 14px", borderRadius: 6, background: rookie ? "var(--brand-ink)" : "transparent", color: rookie ? "#fff" : "var(--brand-ink)" }}
          >
            Rookies only
          </button>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as AthleteSort)}
            aria-label="Sort athletes"
            style={{ border: 0, background: "transparent", fontSize: 13.5, padding: "9px 8px", color: "var(--brand-ink)", outline: "none" }}
          >
            {SORT_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "baseline", gap: 14 }}>
        <span style={{ font: `500 12px ${FONT_MONO}`, letterSpacing: "0.16em", color: "var(--brand-ink)" }}>ALL ATHLETES</span>
        <span style={{ font: `400 12px ${FONT_MONO}`, letterSpacing: "0.12em", color: "var(--brand-slate)" }}>{countLabel}</span>
      </div>

      {tiles.length === 0 ? (
        <p style={{ margin: 0, fontSize: 15, color: "var(--brand-slate)" }}>No athletes match. Try another sport or name.</p>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))", gap: "28px 16px" }}>
          {tiles.map((t) => {
            const href = athleteHref(t.pageKind, t.slug) ?? "#";
            const rookieChip = isRecentRookie(t.rookieYear);
            return (
              <Link key={`${t.pageKind}-${t.slug}`} href={href} style={{ display: "flex", flexDirection: "column", gap: 10, color: "var(--brand-ink)" }}>
                <MonogramTile name={t.name} sport={t.sport} league={t.league} trending={t.trending} />
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  <span style={{ font: `600 15px/1.25 ${FONT_DISPLAY}`, letterSpacing: "-0.01em" }}>{t.name}</span>
                  <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                    <span style={{ fontSize: 12, padding: "4px 9px", background: "var(--brand-track)", border: "1px solid var(--brand-line)", borderRadius: 3 }}>
                      {t.league ?? t.sport}
                    </span>
                    {rookieChip && (
                      <span style={{ fontSize: 12, padding: "4px 9px", background: "var(--brand-ink)", color: "#fff", borderRadius: 3 }}>Rookie</span>
                    )}
                  </div>
                  <div style={{ display: "flex", gap: 14, font: `400 11px ${FONT_MONO}`, color: "var(--brand-slate)" }}>
                    <span>
                      <span style={{ color: "var(--brand-ink)", fontWeight: 500 }}>{t.setCount}</span> sets
                    </span>
                    <span>
                      <span style={{ color: "var(--brand-ink)", fontWeight: 500 }}>{t.cardCount}</span> cards
                    </span>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}

      {hasMore && (
        <div style={{ display: "flex", justifyContent: "center", marginTop: 8 }}>
          <button
            onClick={() => fetchPage(page + 1, true)}
            disabled={loading}
            className="ui-btn ui-btn-md ui-btn-sec"
            style={{ minWidth: 160 }}
          >
            {loading ? "Loading…" : "Load more"}
          </button>
        </div>
      )}
    </main>
  );
}
