import React from "react";
import { ParallelTable, type ParallelRowData } from "./ParallelTable";

const FONT_DISPLAY = "var(--cl-font-display), 'Inter Tight', sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

export interface Chip {
  label: string;
  accent?: boolean;
}

/** Muted metadata pill on subset headers (accent variant for BOOKLET). */
export function TypeChip({ label, accent = false }: { label: string; accent?: boolean }) {
  return (
    <span style={{
      flexShrink: 0,
      fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1, textTransform: "uppercase",
      padding: "2px 6px", borderRadius: 4,
      color: accent ? "#9A2B14" : "#8A8677",
      background: accent ? "rgba(154,43,20,0.07)" : "#F1EFE9",
      border: accent ? "1px solid rgba(154,43,20,0.18)" : "1px solid #E6E3D9",
    }}>{label}</span>
  );
}

/**
 * One subset: header ("<name>  N cards · M parallels" + chips), an optional
 * always-on checklist container, and the adaptive parallels table. Shared by the
 * set page (SubsetSection) and the athlete page tabs so both render identically.
 */
export function SubsetCard({ name, cardsCount, parallelsCount, chips = [], checklist, tableRows, showNumbered }: {
  name: string;
  cardsCount: number;
  parallelsCount: number;
  chips?: Chip[];
  checklist?: React.ReactNode;
  tableRows: ParallelRowData[];
  showNumbered: boolean;
}) {
  return (
    <section style={{ marginBottom: 28 }}>
      <div className="flex flex-wrap items-center gap-2" style={{ marginBottom: 10 }}>
        <h3 style={{ fontFamily: FONT_DISPLAY, fontSize: 18, fontWeight: 600, color: "var(--brand-ink)", margin: 0 }}>
          {name}
        </h3>
        {chips.map((c) => <TypeChip key={c.label} label={c.label} accent={c.accent} />)}
        <span style={{ fontFamily: FONT_MONO, fontSize: 12, color: "#8A8677" }}>
          {cardsCount} card{cardsCount !== 1 ? "s" : ""}
          {parallelsCount > 0 ? ` · ${parallelsCount} parallel${parallelsCount !== 1 ? "s" : ""}` : ""}
        </span>
      </div>
      {checklist}
      {tableRows.length > 0 && <ParallelTable rows={tableRows} showNumbered={showNumbered} />}
    </section>
  );
}
