import React from "react";

const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

export function printRunDisplay(pr: number | null | undefined): string {
  if (pr === undefined || pr === null) return "—";
  if (pr === 1) return "1/1";
  return `/${pr}`;
}

/** Resolved odds cell content: display text plus optional format tag (e.g. "· Jumbo"). */
export interface OddsCell {
  text: string;
  tag?: string | null;
}

export interface ParallelRowData {
  name: string;
  printRun: number | null;
  /** Note surfaced on a "—" cell (dotted underline + hover title). */
  note?: string | null;
  /** Resolved odds, or null → renders "—" (or a note dash). */
  odds: OddsCell | null;
  /** eBay affiliate URL. Present on any row → the table shows the EBAY column. */
  shopUrl?: string | null;
  /** Highlight the parallel name in accent red (rare parallel rule). */
  rare?: boolean;
}

/**
 * Adaptive parallels table shared by the set page and the athlete page.
 * Columns: PARALLEL · [NUMBERED] · [PACK ODDS] · [EBAY]. A column appears only
 * when at least one row needs it, so the set page (no shopUrl) renders exactly
 * the 3-column table it always has.
 */
export function ParallelTable({ rows, showNumbered }: { rows: ParallelRowData[]; showNumbered: boolean }) {
  const showOdds = rows.some((r) => r.odds != null);
  const showNumberedCol = showNumbered && rows.some((r) => r.printRun != null);
  const showEbay = rows.some((r) => r.shopUrl != null);

  const hCell: React.CSSProperties = {
    fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.4,
    color: "#8A8677", textTransform: "uppercase",
  };

  // One grid template drives BOTH the header row and every body row, so the
  // columns register exactly (no independently-sized header/body). Tracks are
  // added only for the columns that are present. Numbered/odds widths match the
  // set page's previous fixed widths so it stays visually unchanged; the eBay
  // track is fixed so it can never squeeze the odds column.
  const tracks = ["minmax(0,1fr)"];
  if (showNumberedCol) tracks.push("72px");
  if (showOdds) tracks.push("132px");
  if (showEbay) tracks.push("120px");
  const rowGrid: React.CSSProperties = {
    display: "grid", gridTemplateColumns: tracks.join(" "), alignItems: "center", padding: "8px 12px",
  };
  // eBay cell/header share left padding so the header label sits over the link.
  const ebayCell: React.CSSProperties = { textAlign: "left", paddingLeft: 12 };

  return (
    <div style={{ marginTop: 12, border: "1px solid #EDEAE0", borderRadius: 8, overflow: "hidden", background: "#FFFFFF" }}>
      <div style={{ ...rowGrid, borderBottom: "1px solid #EDEAE0" }}>
        <span style={hCell}>Parallel</span>
        {showNumberedCol && <span style={{ textAlign: "right", ...hCell }}>Numbered</span>}
        {showOdds && <span style={{ textAlign: "right", ...hCell }}>Pack Odds</span>}
        {showEbay && <span style={{ ...ebayCell, ...hCell }}>eBay</span>}
      </div>
      {rows.map((r, i) => (
        <div key={`${r.name}-${i}`} style={{ ...rowGrid, borderTop: i > 0 ? "1px solid #F4F1E8" : undefined }}>
          <span style={{ fontSize: 14, color: r.rare ? "#9A2B14" : "#0F0F0E", minWidth: 0 }}>{r.name}</span>
          {showNumberedCol && <span style={{ textAlign: "right", fontFamily: FONT_MONO, fontSize: 14, color: "#0F0F0E" }}>{printRunDisplay(r.printRun)}</span>}
          {showOdds && (
            <span style={{ textAlign: "right", fontFamily: FONT_MONO, fontSize: 14, color: "#0F0F0E" }}>
              {r.odds != null ? (
                <>{r.odds.text}{r.odds.tag && <span style={{ color: "#8A8677", fontSize: 11 }}> · {r.odds.tag}</span>}</>
              ) : (r.note ? <span title={r.note} style={{ color: "#8A8677", borderBottom: "1px dotted #B7B2A3", cursor: "help" }}>—</span> : "—")}
            </span>
          )}
          {showEbay && (
            <span style={ebayCell}>
              {r.shopUrl ? (
                <a href={r.shopUrl} target="_blank" rel="sponsored noopener" aria-label="Find on eBay"
                  style={{ fontFamily: FONT_MONO, fontSize: 12, fontWeight: 600, color: "#B12C18", textDecoration: "none", whiteSpace: "nowrap" }}>
                  <span className="hidden min-[1180px]:inline">Find on eBay </span>↗
                </a>
              ) : null}
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
