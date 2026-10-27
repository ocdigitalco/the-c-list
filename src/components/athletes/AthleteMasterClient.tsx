"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { MonogramBadge } from "./MonogramTile";
import { LastSoldControl } from "@/components/sets/LastSoldControl";
import { sportTint } from "@/lib/athletes/util";
import type { AthletePageData, AllCardRow } from "@/lib/athletes/queries";

const FONT_DISPLAY = "var(--cl-font-display), var(--brand-font-head), system-ui, sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

type Tab = "Overview" | "All Cards" | "By Set" | "Autographs" | "Numbered" | "Rookies" | "Teams";
type RailTab = "Sets" | "Teams" | "Years";
type RailSort = "cards" | "autos" | "inserts" | "numbered" | "ones";
type SalesFilter = "All" | "Raw" | "Graded" | "Autos" | "Numbered";

const lbl: React.CSSProperties = {
  font: `500 10px ${FONT_MONO}`,
  letterSpacing: "0.12em",
  color: "var(--brand-slate)",
  textTransform: "uppercase",
};
const panel: React.CSSProperties = {
  background: "var(--brand-card)",
  border: "1px solid var(--brand-line)",
  borderRadius: 12,
};

function money(cents: number | null): string {
  if (cents == null) return "—";
  const d = cents / 100;
  return d >= 1000 ? `$${d.toLocaleString(undefined, { maximumFractionDigits: 0 })}` : `$${d.toFixed(2)}`;
}

function fmtDate(iso: string | null): string {
  if (!iso) return "—";
  const d = new Date(iso.length <= 10 ? iso + "T00:00:00Z" : iso);
  if (isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" });
}

export function AthleteMasterClient({
  data,
  soldCompsEnabled,
  ebayAllUrl,
}: {
  data: AthletePageData;
  soldCompsEnabled: boolean;
  ebayAllUrl: string | null;
}) {
  const { athlete, stats, teams, cardsBySet, gallery, cardsPerYear, hardestToPull, rightCard, allCards, rail, recentSales, recentSalesPricedCount } = data;

  const [tab, setTab] = useState<Tab>("Overview");
  const [railTab, setRailTab] = useState<RailTab>("Sets");
  const [railQuery, setRailQuery] = useState("");
  const [railSort, setRailSort] = useState<RailSort>("cards");
  const [railRookieOnly, setRailRookieOnly] = useState(false);
  const [railLimit, setRailLimit] = useState(9);
  const [cardsLimit, setCardsLimit] = useState(50);
  const [salesFilter, setSalesFilter] = useState<SalesFilter>("All");
  const [cardsBySetLimit, setCardsBySetLimit] = useState(6);
  const [galleryLimit] = useState(9);
  const [mobileRailOpen, setMobileRailOpen] = useState(false);

  const yearSpan =
    data.yearRange && data.yearRange.from !== data.yearRange.to
      ? `${data.yearRange.from}–${data.yearRange.to}`
      : data.yearRange
        ? `${data.yearRange.from}`
        : null;

  // Rail rows filtered + sorted.
  const railRows = useMemo(() => {
    let rows = rail;
    const q = railQuery.trim().toLowerCase();
    if (q) rows = rows.filter((r) => r.setName.toLowerCase().includes(q));
    if (railRookieOnly) rows = rows.filter((r) => r.isRookieYear);
    const key = railSort;
    return [...rows].sort((a, b) => (b[key] as number) - (a[key] as number) || b.cards - a.cards || a.setName.localeCompare(b.setName));
  }, [rail, railQuery, railRookieOnly, railSort]);

  const tabCards = useMemo(() => {
    switch (tab) {
      case "Autographs":
        return allCards.filter((c) => c.isAutograph);
      case "Numbered":
        return allCards.filter((c) => c.isNumbered);
      case "Rookies":
        return allCards.filter((c) => c.isRookie);
      default:
        return allCards;
    }
  }, [tab, allCards]);

  const filteredSales = useMemo(() => {
    switch (salesFilter) {
      case "Raw":
        return recentSales.filter((s) => !s.isGraded);
      case "Graded":
        return recentSales.filter((s) => s.isGraded);
      case "Autos":
        return recentSales.filter((s) => s.isAutograph);
      case "Numbered":
        return recentSales.filter((s) => s.isNumbered);
      default:
        return recentSales;
    }
  }, [salesFilter, recentSales]);

  const maxYear = Math.max(1, ...cardsPerYear.map((y) => y.count));
  const nowYear = new Date().getUTCFullYear();

  const TABS: Tab[] = ["Overview", "All Cards", "By Set", "Autographs", "Numbered", "Rookies", "Teams"];
  const tabCount = (t: Tab): number | null => {
    if (t === "All Cards") return allCards.length;
    if (t === "Autographs") return stats.autographs;
    if (t === "Numbered") return stats.numbered;
    if (t === "Rookies") return stats.rookieCards;
    return null;
  };

  // ── Rail (shared desktop + mobile) ──────────────────────────────────────────
  const railNode = (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div style={{ display: "flex", gap: 22, padding: "0 4px", borderBottom: "1px solid var(--brand-line)" }}>
        {(["Sets", "Teams", "Years"] as RailTab[]).map((t) => {
          const n = t === "Sets" ? rail.length : t === "Teams" ? teams.length : cardsPerYear.length;
          const active = railTab === t;
          return (
            <button
              key={t}
              onClick={() => setRailTab(t)}
              style={{
                border: 0,
                background: "transparent",
                cursor: "pointer",
                font: `${active ? 600 : 500} 14px ${FONT_DISPLAY}`,
                color: active ? "var(--brand-ink)" : "var(--brand-slate)",
                padding: "14px 2px 12px",
                borderBottom: active ? "2px solid var(--brand-accent)" : "2px solid transparent",
              }}
            >
              {t} ({n})
            </button>
          );
        })}
      </div>

      {railTab === "Sets" && (
        <>
          <div style={{ padding: "16px 12px 12px", display: "flex", flexDirection: "column", gap: 12, borderBottom: "1px solid var(--brand-line)" }}>
            <input
              value={railQuery}
              onChange={(e) => setRailQuery(e.target.value)}
              placeholder="Search their sets…"
              aria-label="Search their sets"
              style={{ background: "var(--brand-field)", border: "1px solid var(--brand-line)", borderRadius: 8, padding: "10px 12px", fontSize: 14, outline: "none", color: "var(--brand-ink)" }}
            />
            <div style={{ display: "flex", flexWrap: "wrap", gap: 7 }}>
              {([
                ["cards", "Total Cards"],
                ["autos", "Autos"],
                ["inserts", "Inserts"],
                ["numbered", "Numbered"],
                ["ones", "1/1s"],
              ] as [RailSort, string][]).map(([k, label]) => {
                const active = railSort === k;
                return (
                  <button
                    key={k}
                    onClick={() => setRailSort(k)}
                    aria-pressed={active}
                    style={{
                      font: `${active ? 600 : 500} 12.5px ${FONT_DISPLAY}`,
                      color: active ? "#fff" : "var(--brand-slate)",
                      background: active ? "var(--brand-ink)" : "var(--brand-card)",
                      border: active ? 0 : "1px solid var(--brand-line)",
                      borderRadius: 6,
                      padding: "7px 12px",
                      cursor: "pointer",
                    }}
                  >
                    {label}
                  </button>
                );
              })}
            </div>
            <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13.5, color: "var(--brand-slate)", cursor: "pointer" }}>
              <input type="checkbox" checked={railRookieOnly} onChange={(e) => setRailRookieOnly(e.target.checked)} />
              Rookie-year sets only
            </label>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", padding: "12px 12px 8px" }}>
            <span style={lbl}>Set</span>
            <span style={lbl}>Cards</span>
          </div>
          {railRows.slice(0, railLimit).map((r, i) => (
            <Link
              key={r.setId}
              href={r.setHref}
              style={{ display: "flex", gap: 12, alignItems: "center", padding: "12px", borderTop: "1px solid var(--brand-line)", color: "var(--brand-ink)", background: i % 2 ? "transparent" : "var(--brand-sel)" }}
            >
              <span style={{ font: `500 12px ${FONT_MONO}`, color: "var(--brand-slate)", width: 16 }}>{i + 1}</span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ font: `600 14px ${FONT_DISPLAY}` }}>{r.setName}</div>
                <div style={{ fontSize: 12, color: "var(--brand-slate)", marginTop: 2 }}>
                  {r.sport} · {r.cardTypes} card type{r.cardTypes === 1 ? "" : "s"}
                  {r.isRookieYear ? " · Rookie year" : ""}
                </div>
              </div>
              <span style={{ font: `600 16px ${FONT_MONO}`, color: "var(--brand-ink)" }}>{r.cards}</span>
            </Link>
          ))}
          {railRows.length > railLimit && (
            <button onClick={() => setRailLimit((n) => n + 20)} style={{ border: 0, background: "transparent", cursor: "pointer", textAlign: "left", padding: "14px 12px 18px", font: `600 13.5px ${FONT_DISPLAY}`, color: "var(--brand-accent-deep)" }}>
              Show {railRows.length - railLimit} more set{railRows.length - railLimit === 1 ? "" : "s"}
            </button>
          )}
          {railRows.length === 0 && <div style={{ padding: 16, fontSize: 13, color: "var(--brand-slate)" }}>No sets match.</div>}
        </>
      )}

      {railTab === "Teams" && (
        <div style={{ padding: 14, display: "flex", flexDirection: "column", gap: 14 }}>
          {teams.map((t) => (
            <div key={t.name}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14, marginBottom: 6 }}>
                <span>{t.name}</span>
                <span style={{ fontFamily: FONT_MONO, color: "var(--brand-slate)" }}>{t.cards}</span>
              </div>
              <div style={{ height: 7, background: "var(--brand-track)", borderRadius: 4 }}>
                <div style={{ width: `${t.pct}%`, height: 7, background: "var(--brand-ink)", borderRadius: 4 }} />
              </div>
            </div>
          ))}
          {teams.length === 0 && <div style={{ fontSize: 13, color: "var(--brand-slate)" }}>No team data on their cards.</div>}
        </div>
      )}

      {railTab === "Years" && (
        <div style={{ padding: 14, display: "flex", flexDirection: "column" }}>
          {[...cardsPerYear].reverse().map((y) => (
            <div key={y.year} style={{ display: "flex", justifyContent: "space-between", padding: "10px 2px", borderBottom: "1px solid var(--brand-line)", fontSize: 14 }}>
              <span>{y.year}</span>
              <span style={{ fontFamily: FONT_MONO, color: "var(--brand-slate)" }}>{y.count}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  // ── Appearance table (All Cards / Autographs / Numbered / Rookies / By Set) ──
  const cardRow = (c: AllCardRow) => (
    <div
      key={c.paId}
      style={{ display: "grid", gridTemplateColumns: "minmax(0,1fr) 92px 92px 160px", gap: "0 14px", alignItems: "center", padding: "11px 0", borderTop: "1px solid var(--brand-line)" }}
      className="athlete-card-row"
    >
      <div style={{ minWidth: 0 }}>
        <Link href={c.setHref} style={{ font: `600 14px ${FONT_DISPLAY}`, color: "var(--brand-ink)" }}>
          {c.subset ?? "Base"} #{c.cardNumber}
        </Link>
        <div style={{ fontSize: 12, color: "var(--brand-slate)", marginTop: 2 }}>{c.setName}</div>
      </div>
      <span style={{ textAlign: "right", font: `400 13px ${FONT_MONO}`, color: "var(--brand-slate)" }}>
        {c.parallelCount > 0 ? `${c.parallelCount} parallel${c.parallelCount === 1 ? "" : "s"}` : "—"}
      </span>
      <span style={{ textAlign: "right", font: `500 13px ${FONT_MONO}`, color: c.isOneOfOne ? "var(--brand-accent-deep)" : "var(--brand-ink)" }}>
        {c.printRunLabel ?? "—"}
      </span>
      <div style={{ display: "flex", justifyContent: "flex-end", alignItems: "center", gap: 10 }}>
        {soldCompsEnabled && (
          <LastSoldControl setId={c.setId} insertSetId={c.insertSetId} cardNumber={c.cardNumber} playerId={c.playerId} />
        )}
        {c.ebayUrl && (
          <a href={c.ebayUrl} target="_blank" rel="sponsored noopener" style={{ font: `600 12px ${FONT_MONO}`, color: "var(--brand-accent-deep)", whiteSpace: "nowrap" }}>
            eBay ↗
          </a>
        )}
      </div>
    </div>
  );

  const appearanceTable = (rows: AllCardRow[]) => (
    <div style={{ ...panel, padding: "16px 18px 8px" }}>
      <div style={{ display: "grid", gridTemplateColumns: "minmax(0,1fr) 92px 92px 160px", gap: "0 14px", padding: "0 0 8px" }}>
        <span style={lbl}>Card</span>
        <span style={{ ...lbl, textAlign: "right" }}>Parallels</span>
        <span style={{ ...lbl, textAlign: "right" }}>Print Run</span>
        <span style={{ ...lbl, textAlign: "right" }}>Market</span>
      </div>
      {rows.slice(0, cardsLimit).map(cardRow)}
      {rows.length > cardsLimit && (
        <button onClick={() => setCardsLimit((n) => n + 100)} style={{ border: 0, background: "transparent", cursor: "pointer", padding: "14px 0 16px", font: `600 13.5px ${FONT_DISPLAY}`, color: "var(--brand-accent-deep)" }}>
          Show {rows.length - cardsLimit} more
        </button>
      )}
      {rows.length === 0 && <div style={{ padding: "16px 0", fontSize: 13, color: "var(--brand-slate)" }}>None.</div>}
    </div>
  );

  // Group rows by set for the By Set tab.
  const bySet = useMemo(() => {
    const m = new Map<number, { setName: string; setHref: string; rows: AllCardRow[] }>();
    for (const c of allCards) {
      const g = m.get(c.setId) ?? { setName: c.setName, setHref: c.setHref, rows: [] };
      g.rows.push(c);
      m.set(c.setId, g);
    }
    return Array.from(m.values()).sort((a, b) => b.rows.length - a.rows.length);
  }, [allCards]);

  return (
    <div style={{ background: "var(--brand-page)" }}>
      <div className="grid grid-cols-1 min-[980px]:grid-cols-[300px_minmax(0,1fr)]">
        {/* Rail — desktop */}
        <aside className="hidden min-[980px]:block" style={{ borderRight: "1px solid var(--brand-line)", background: "var(--brand-head)", alignSelf: "start", position: "sticky", top: "var(--header-h, 56px)" }}>
          {railNode}
        </aside>

        {/* Content */}
        <div style={{ minWidth: 0 }}>
          <div style={{ padding: "18px 16px 0", font: "400 14px sans-serif", color: "var(--brand-slate)" }}>
            <Link href="/athletes" style={{ color: "var(--brand-slate)" }}>
              ‹ Athletes
            </Link>{" "}
            · {athlete.sport}
          </div>

          {/* Mobile rail toggle */}
          <div className="min-[980px]:hidden" style={{ padding: "12px 16px 0" }}>
            <button onClick={() => setMobileRailOpen((o) => !o)} className="ui-btn ui-btn-sm ui-btn-sec" style={{ width: "100%" }}>
              {mobileRailOpen ? "Hide their sets" : `Their sets (${rail.length})`}
            </button>
            {mobileRailOpen && <div style={{ ...panel, marginTop: 12 }}>{railNode}</div>}
          </div>

          {/* Header */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 26, alignItems: "flex-start", padding: "16px 16px 22px" }}>
            <MonogramBadge name={athlete.name} sport={athlete.sport} />
            <div style={{ flex: 1, minWidth: 240, paddingTop: 4 }}>
              {teams.length > 0 && (
                <div style={{ ...lbl, marginBottom: 8 }}>{teams.slice(0, 3).map((t) => t.name).join(" · ").toUpperCase()}</div>
              )}
              <h1 className="page-title" style={{ margin: 0, fontSize: 46, lineHeight: 1.02, letterSpacing: "-0.01em" }}>
                {athlete.name}
              </h1>
              <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 16, flexWrap: "wrap" }}>
                <span style={{ fontSize: 14, background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 7, padding: "9px 15px" }}>{athlete.sport}</span>
                {teams[0] && (
                  <span style={{ fontSize: 14, background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 7, padding: "9px 15px" }}>{teams[0].name}</span>
                )}
                <span style={{ fontSize: 14.5, color: "var(--brand-slate)" }}>
                  {stats.totalCards} cards across {stats.sets} set{stats.sets === 1 ? "" : "s"}
                  {yearSpan ? ` · ${yearSpan}` : ""}
                </span>
              </div>
              {rightCard.aliases.length > 0 && (
                <div style={{ marginTop: 12, fontSize: 13.5, color: "var(--brand-slate)" }}>
                  <span style={{ fontWeight: 600, color: "var(--brand-ink)" }}>Also known as</span> {rightCard.aliases.join(", ")}
                </div>
              )}
            </div>
            {/* Facts card */}
            <div style={{ ...panel, background: "var(--brand-head)", padding: "16px 18px", minWidth: 260 }}>
              <div style={{ ...lbl, marginBottom: 14 }}>This subject</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 10, fontSize: 14 }}>
                {rightCard.newestSet && (
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                    <span>Newest set</span>
                    <span style={{ color: "var(--brand-slate)", textAlign: "right" }}>{rightCard.newestSet.name}</span>
                  </div>
                )}
                {rightCard.rookie && (
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span>Rookie year</span>
                    <span style={{ color: "var(--brand-slate)" }}>
                      {rightCard.rookie.year} · {rightCard.rookie.cards} card{rightCard.rookie.cards === 1 ? "" : "s"}
                    </span>
                  </div>
                )}
                {rightCard.upcomingCount > 0 && (
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span>Upcoming sets</span>
                    <span style={{ color: "var(--brand-accent-deep)" }}>{rightCard.upcomingCount} announced</span>
                  </div>
                )}
                {ebayAllUrl && (
                  <a href={ebayAllUrl} target="_blank" rel="sponsored noopener" style={{ marginTop: 4, font: `600 13px ${FONT_DISPLAY}`, color: "var(--brand-accent-deep)" }}>
                    Find on eBay — all sets ↗
                  </a>
                )}
              </div>
            </div>
          </div>

          {/* Stats strip */}
          <div
            className="grid grid-cols-2 min-[720px]:grid-cols-3 min-[1180px]:grid-cols-6"
            style={{ borderTop: "1px solid var(--brand-line)", borderBottom: "1px solid var(--brand-line)", background: "var(--brand-head)" }}
          >
            {([
              ["Sets", stats.sets],
              ["Total Cards", stats.totalCards],
              ["Autographs", stats.autographs],
              ["Numbered", stats.numbered],
              ["1/1s", stats.ones],
              ["Rookie Cards", stats.rookieCards],
            ] as [string, number][]).map(([label, val]) => (
              <div key={label} style={{ padding: "16px 20px", borderRight: "1px solid var(--brand-line)", borderTop: "1px solid var(--brand-line)" }}>
                <div style={lbl}>{label}</div>
                <div className="page-title" style={{ fontSize: 30, marginTop: 6 }}>{val}</div>
              </div>
            ))}
          </div>

          {/* Content tabs */}
          <div style={{ display: "flex", gap: 26, padding: "0 16px", borderBottom: "1px solid var(--brand-line)", overflowX: "auto" }}>
            {TABS.map((t) => {
              const n = tabCount(t);
              const active = tab === t;
              return (
                <button
                  key={t}
                  onClick={() => {
                    setTab(t);
                    setCardsLimit(50);
                  }}
                  style={{
                    border: 0,
                    background: "transparent",
                    cursor: "pointer",
                    whiteSpace: "nowrap",
                    font: `${active ? 600 : 500} 15px ${FONT_DISPLAY}`,
                    color: active ? "var(--brand-ink)" : "var(--brand-slate)",
                    padding: "16px 2px 13px",
                    borderBottom: active ? "2px solid var(--brand-accent)" : "2px solid transparent",
                  }}
                >
                  {t}
                  {n != null ? ` (${n})` : ""}
                </button>
              );
            })}
          </div>

          <div style={{ padding: "24px 16px 48px", display: "flex", flexDirection: "column", gap: 28 }}>
            {tab === "Overview" && (
              <>
                {/* Card gallery (set art only) */}
                <section>
                  <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 12 }}>
                    <span style={lbl}>Card gallery · all sets</span>
                    <button onClick={() => setTab("All Cards")} style={{ border: 0, background: "transparent", cursor: "pointer", font: `500 13px ${FONT_DISPLAY}`, color: "var(--brand-accent-deep)" }}>
                      View all {allCards.length} ›
                    </button>
                  </div>
                  <div className="grid grid-cols-3 min-[720px]:grid-cols-5 min-[1180px]:grid-cols-9" style={{ gap: 14 }}>
                    {gallery.slice(0, galleryLimit).map((g) => (
                      <Link key={g.setId} href={g.setHref} style={{ display: "flex", flexDirection: "column", border: "1px solid var(--brand-line)", borderRadius: 8, overflow: "hidden", background: "var(--brand-card)", color: "inherit" }}>
                        <div style={{ position: "relative", aspectRatio: "5 / 7", background: g.image ? "var(--brand-ph)" : sportTint(athlete.sport) }}>
                          {g.image ? (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img src={g.image} alt="" loading="lazy" style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
                          ) : (
                            <span style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", font: `italic 800 28px ${FONT_DISPLAY}`, opacity: 0.9 }}>
                              {athlete.sport.slice(0, 1)}
                            </span>
                          )}
                          <span style={{ position: "absolute", bottom: 0, left: 0, right: 0, padding: "5px 7px", background: "rgba(0,0,0,.74)", color: "#fff", font: `600 9.5px ${FONT_MONO}`, letterSpacing: "0.04em" }}>
                            {g.chip}
                          </span>
                        </div>
                        <div style={{ padding: "8px 9px 10px", fontSize: 10.5, lineHeight: 1.3, color: "var(--brand-slate)" }}>{g.setName}</div>
                      </Link>
                    ))}
                  </div>
                </section>

                <div className="grid grid-cols-1 min-[980px]:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]" style={{ gap: 24, alignItems: "start" }}>
                  <div style={{ display: "flex", flexDirection: "column", gap: 22 }}>
                    {/* Cards by set */}
                    <section style={{ ...panel, padding: "20px 20px 10px" }}>
                      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", paddingBottom: 12, borderBottom: "1px solid var(--brand-line)" }}>
                        <span style={{ font: `700 18px ${FONT_DISPLAY}` }}>Cards by set</span>
                        <span style={{ fontSize: 13, color: "var(--brand-slate)" }}>by their card count</span>
                      </div>
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 52px 52px 62px 40px", gap: "0 14px", padding: "12px 0 8px" }}>
                        <span style={lbl}>Set</span>
                        <span style={{ ...lbl, textAlign: "right" }}>Cards</span>
                        <span style={{ ...lbl, textAlign: "right" }}>Autos</span>
                        <span style={{ ...lbl, textAlign: "right" }}>Numb.</span>
                        <span style={{ ...lbl, textAlign: "right" }}>1/1s</span>
                      </div>
                      {cardsBySet.slice(0, cardsBySetLimit).map((s) => (
                        <div key={s.setId} style={{ display: "grid", gridTemplateColumns: "1fr 52px 52px 62px 40px", gap: "0 14px", alignItems: "center", padding: "12px 0", borderTop: "1px solid var(--brand-line)" }}>
                          <div style={{ minWidth: 0 }}>
                            <Link href={s.setHref} style={{ fontWeight: 600, fontSize: 14.5, color: "var(--brand-ink)" }}>{s.setName}</Link>
                            <div style={{ fontSize: 12, color: "var(--brand-slate)", marginTop: 2 }}>
                              {[s.manufacturer, fmtDate(s.releaseDate) !== "—" ? fmtDate(s.releaseDate) : null].filter(Boolean).join(" · ")}
                            </div>
                          </div>
                          <span style={{ textAlign: "right", font: `600 14px ${FONT_MONO}` }}>{s.cards}</span>
                          <span style={{ textAlign: "right", font: `400 14px ${FONT_MONO}`, color: "var(--brand-slate)" }}>{s.autos}</span>
                          <span style={{ textAlign: "right", font: `400 14px ${FONT_MONO}`, color: "var(--brand-slate)" }}>{s.numbered}</span>
                          <span style={{ textAlign: "right", font: `400 14px ${FONT_MONO}`, color: "var(--brand-slate)" }}>{s.ones}</span>
                        </div>
                      ))}
                      {cardsBySet.length > cardsBySetLimit && (
                        <button onClick={() => setCardsBySetLimit(cardsBySet.length)} style={{ border: 0, background: "transparent", cursor: "pointer", padding: "14px 0 16px", font: `600 13.5px ${FONT_DISPLAY}`, color: "var(--brand-accent-deep)" }}>
                          Show all {cardsBySet.length} sets
                        </button>
                      )}
                    </section>

                    {/* Teams on their cards */}
                    {teams.length > 0 && (
                      <section style={{ ...panel, background: "var(--brand-head)", padding: "20px 20px 22px" }}>
                        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 16 }}>
                          <span style={{ font: `700 18px ${FONT_DISPLAY}` }}>Teams on their cards</span>
                          <span style={{ fontSize: 13, color: "var(--brand-slate)" }}>{teams.length} team{teams.length === 1 ? "" : "s"} · {stats.totalCards} cards</span>
                        </div>
                        <div className="grid grid-cols-1 min-[560px]:grid-cols-2" style={{ gap: "14px 26px" }}>
                          {teams.slice(0, 8).map((t) => (
                            <div key={t.name}>
                              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14, marginBottom: 6 }}>
                                <span>{t.name}</span>
                                <span style={{ fontFamily: FONT_MONO, color: "var(--brand-slate)" }}>{t.cards}</span>
                              </div>
                              <div style={{ height: 7, background: "var(--brand-track)", borderRadius: 4 }}>
                                <div style={{ width: `${t.pct}%`, height: 7, background: "var(--brand-ink)", borderRadius: 4 }} />
                              </div>
                            </div>
                          ))}
                        </div>
                      </section>
                    )}
                  </div>

                  <div style={{ display: "flex", flexDirection: "column", gap: 22 }}>
                    {/* Cards per year */}
                    {cardsPerYear.length > 0 && (
                      <section style={{ ...panel, padding: "20px 20px 22px" }}>
                        <div style={{ font: `700 18px ${FONT_DISPLAY}`, marginBottom: 4 }}>Cards per year</div>
                        <div style={{ fontSize: 13, color: "var(--brand-slate)", marginBottom: 18 }}>Every card printed of them, by release year</div>
                        <div style={{ display: "flex", alignItems: "flex-end", gap: 10, height: 150 }}>
                          {cardsPerYear.map((y) => {
                            const cur = y.year === nowYear;
                            return (
                              <div key={y.year} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
                                <span style={{ font: `500 11px ${FONT_MONO}`, color: cur ? "var(--brand-accent-deep)" : "var(--brand-slate)" }}>{y.count}</span>
                                <div style={{ width: "100%", height: Math.max(6, Math.round((y.count / maxYear) * 120)), background: cur ? "var(--brand-accent)" : "var(--brand-fog)", borderRadius: "4px 4px 0 0" }} />
                                <span style={{ font: `400 11px ${FONT_MONO}`, color: cur ? "var(--brand-accent-deep)" : "var(--brand-slate)" }}>'{String(y.year).slice(2)}</span>
                              </div>
                            );
                          })}
                        </div>
                      </section>
                    )}

                    {/* Hardest to pull */}
                    {hardestToPull.length > 0 && (
                      <section style={{ ...panel, padding: "20px 20px 10px" }}>
                        <div style={{ font: `700 18px ${FONT_DISPLAY}`, marginBottom: 8 }}>Hardest to pull</div>
                        {hardestToPull.map((h, i) => (
                          <div key={i} style={{ display: "flex", alignItems: "center", gap: 14, padding: "12px 0", borderTop: i > 0 ? "1px solid var(--brand-line)" : undefined }}>
                            <div style={{ flex: 1, minWidth: 0 }}>
                              <div style={{ font: `600 14.5px ${FONT_DISPLAY}` }}>{h.parallelName}</div>
                              <div style={{ fontSize: 12, color: "var(--brand-slate)", marginTop: 2 }}>{h.setName}</div>
                            </div>
                            <span style={{ font: `600 13px ${FONT_MONO}`, color: h.printRun === 1 ? "var(--brand-accent-deep)" : "var(--brand-slate)", background: h.printRun === 1 ? "var(--brand-tint)" : "var(--brand-track)", border: "1px solid var(--brand-line)", borderRadius: 5, padding: "5px 8px" }}>
                              {h.printRun === 1 ? "1/1" : `/${h.printRun}`}
                            </span>
                          </div>
                        ))}
                      </section>
                    )}
                  </div>
                </div>

                {/* Recent sales */}
                <section>
                  <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 12, flexWrap: "wrap", gap: 10 }}>
                    <span style={lbl}>Recent sales · cached lookups</span>
                    {recentSalesPricedCount >= 5 && (
                      <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                        {(["All", "Raw", "Graded", "Autos", "Numbered"] as SalesFilter[]).map((f) => {
                          const active = salesFilter === f;
                          return (
                            <button key={f} onClick={() => setSalesFilter(f)} aria-pressed={active} style={{ font: `${active ? 600 : 500} 12.5px ${FONT_DISPLAY}`, color: active ? "#fff" : "var(--brand-slate)", background: active ? "var(--brand-ink)" : "var(--brand-card)", border: active ? 0 : "1px solid var(--brand-line)", borderRadius: 20, padding: "7px 14px", cursor: "pointer" }}>
                              {f}
                            </button>
                          );
                        })}
                      </div>
                    )}
                  </div>
                  {recentSalesPricedCount < 5 ? (
                    <div style={{ ...panel, padding: "18px 20px", fontSize: 14, color: "var(--brand-slate)" }}>
                      Prices appear as cards are looked up — use Last Sold on any card below.
                    </div>
                  ) : (
                    <div style={{ ...panel, padding: "16px 20px 10px" }}>
                      <div style={{ display: "grid", gridTemplateColumns: "minmax(0,1fr) 72px 120px 72px 96px", gap: "0 14px", padding: "0 0 8px" }}>
                        <span style={lbl}>Card</span>
                        <span style={lbl}>Grade</span>
                        <span style={lbl}>Sale type</span>
                        <span style={lbl}>Date</span>
                        <span style={{ ...lbl, textAlign: "right" }}>Sold for</span>
                      </div>
                      {filteredSales.map((s, i) => (
                        <div key={i} style={{ display: "grid", gridTemplateColumns: "minmax(0,1fr) 72px 120px 72px 96px", gap: "0 14px", alignItems: "center", padding: "11px 0", borderTop: "1px solid var(--brand-line)" }}>
                          <div style={{ minWidth: 0 }}>
                            {s.url ? (
                              <a href={s.url} target="_blank" rel="sponsored noopener" style={{ font: `600 14px ${FONT_DISPLAY}`, color: "var(--brand-ink)" }}>{s.cardLabel}</a>
                            ) : (
                              <span style={{ font: `600 14px ${FONT_DISPLAY}` }}>{s.cardLabel}</span>
                            )}
                            <div style={{ fontSize: 12, color: "var(--brand-slate)", marginTop: 2 }}>{s.setName}</div>
                          </div>
                          <span style={{ font: `600 10.5px ${FONT_MONO}`, color: "var(--brand-slate)" }}>{s.grade}</span>
                          <span style={{ fontSize: 13, color: "var(--brand-slate)" }}>{s.saleType}</span>
                          <span style={{ font: `400 13px ${FONT_MONO}`, color: "var(--brand-slate)" }}>{fmtDate(s.soldAt)}</span>
                          <span style={{ textAlign: "right", font: `600 15px ${FONT_MONO}` }}>{money(s.priceCents)}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  <div style={{ fontSize: 12, lineHeight: 1.5, color: "var(--brand-slate)", padding: "10px 4px 0" }}>
                    Sold data via SoldComps. Grades and parallels are parsed from listing titles and may not be exact.
                  </div>
                </section>
              </>
            )}

            {tab === "By Set" &&
              bySet.map((g) => (
                <section key={g.setName} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
                    <Link href={g.setHref} style={{ font: `700 17px ${FONT_DISPLAY}`, color: "var(--brand-ink)" }}>{g.setName}</Link>
                    <span style={{ fontSize: 13, color: "var(--brand-slate)" }}>{g.rows.length} card{g.rows.length === 1 ? "" : "s"}</span>
                  </div>
                  <div style={{ ...panel, padding: "6px 18px 8px" }}>{g.rows.map(cardRow)}</div>
                </section>
              ))}

            {(tab === "All Cards" || tab === "Autographs" || tab === "Numbered" || tab === "Rookies") && appearanceTable(tabCards)}

            {tab === "Teams" && (
              <section style={{ ...panel, padding: "20px 20px 22px" }}>
                <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 16 }}>
                  <span style={{ font: `700 18px ${FONT_DISPLAY}` }}>Teams on their cards</span>
                  <span style={{ fontSize: 13, color: "var(--brand-slate)" }}>{teams.length} team{teams.length === 1 ? "" : "s"}</span>
                </div>
                {teams.length === 0 ? (
                  <div style={{ fontSize: 14, color: "var(--brand-slate)" }}>No team data on their cards.</div>
                ) : (
                  <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                    {teams.map((t) => (
                      <div key={t.name}>
                        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14, marginBottom: 6 }}>
                          <span>{t.name}</span>
                          <span style={{ fontFamily: FONT_MONO, color: "var(--brand-slate)" }}>{t.cards}</span>
                        </div>
                        <div style={{ height: 7, background: "var(--brand-track)", borderRadius: 4 }}>
                          <div style={{ width: `${t.pct}%`, height: 7, background: "var(--brand-ink)", borderRadius: 4 }} />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
