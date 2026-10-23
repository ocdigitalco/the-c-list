import type { BoxConfigSingle, BoxConfigMulti } from "./types";
import { label as formatBoxLabel } from "@/lib/boxLabels";

const FONT_DISPLAY = "var(--cl-font-display), 'Inter Tight', sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

interface BoxRow {
  label: string;
  cardsPerPack: number | null;
  packsPerBox: number | null;
  boxesPerCase: number | null;
  autosPerBox: number | null;
  notes?: string;
}

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

function getAutosPerBox(fmt: BoxConfigSingle): number | null {
  return fmt.autos_per_box ?? fmt.autos_or_memorabilia_per_box ??
    fmt.autos_or_relics_per_box ?? fmt.autos_or_auto_relics_per_box ?? null;
}

function buildBoxRows(boxConfig: string): BoxRow[] {
  const raw = JSON.parse(boxConfig) as BoxConfigSingle | BoxConfigMulti;
  if (isMultiConfig(raw)) {
    return Object.entries(raw).map(([key, fmt]) => ({
      label: formatBoxLabel(key),
      cardsPerPack: fmt.cards_per_pack ?? null,
      packsPerBox: fmt.packs_per_box ?? null,
      boxesPerCase: fmt.boxes_per_case ?? null,
      autosPerBox: getAutosPerBox(fmt),
      notes: fmt.notes ?? fmt.note ?? undefined,
    }));
  }
  const fmt = raw as BoxConfigSingle;
  return [{
    label: "Hobby",
    cardsPerPack: fmt.cards_per_pack ?? null,
    packsPerBox: fmt.packs_per_box ?? null,
    boxesPerCase: fmt.boxes_per_case ?? null,
    autosPerBox: getAutosPerBox(fmt),
    notes: fmt.notes ?? fmt.note ?? undefined,
  }];
}

// The ordered, de-duplicated format labels the pack-odds panel renders, so the
// table agrees with it. Mirrors PackOddsInline: nested pack_odds keys in
// insertion order, first spelling of a given label wins (e.g. value before
// value_se). Flat or absent odds → empty (caller falls back to box_config order).
function oddsLabelOrder(packOdds: string | null): string[] {
  if (!packOdds) return [];
  let raw: unknown;
  try { raw = JSON.parse(packOdds); } catch { return []; }
  if (!raw || typeof raw !== "object") return [];
  const vals = Object.values(raw as Record<string, unknown>);
  const nested = vals.length > 0 && vals[0] !== null && typeof vals[0] === "object";
  if (!nested) return [];
  const order: string[] = [];
  for (const key of Object.keys(raw as Record<string, unknown>)) {
    const lbl = formatBoxLabel(key);
    if (!order.includes(lbl)) order.push(lbl);
  }
  return order;
}

// Order rows to match the odds panel: odds-listed labels first (in odds order),
// then any box-only labels in their original box_config order. A stable sort
// keeps box-only rows (odds index MAX) in place. When no odds order applies
// (flat/null odds, or keys that don't align), rows keep box_config order.
function orderRows(rows: BoxRow[], packOdds: string | null): BoxRow[] {
  const order = oddsLabelOrder(packOdds);
  if (order.length === 0) return rows;
  const idx = (lbl: string) => {
    const i = order.indexOf(lbl);
    return i === -1 ? Number.MAX_SAFE_INTEGER : i;
  };
  return rows
    .map((r, i) => ({ r, i }))
    .sort((a, b) => (idx(a.r.label) - idx(b.r.label)) || (a.i - b.i))
    .map((x) => x.r);
}

// "—" for a figure the manufacturer has not published. Lighter muted than real
// values; carries an aria-label so the dash isn't read as empty.
function Dash() {
  return (
    <span aria-label="not published" style={{ color: "var(--brand-fog)" }}>—</span>
  );
}

function Num({ value, muted = false }: { value: number | null; muted?: boolean }) {
  if (value == null) return <Dash />;
  return <span style={{ color: muted ? "var(--brand-slate)" : "var(--brand-ink)" }}>{value.toLocaleString()}</span>;
}

// Per-box guarantee: the autograph/relic count first ("1 auto/box"), then any
// free-text note in italic (e.g. "Configuration TBA", "2 RayWave Parallels").
// Both are optional; "—" only when neither is present.
function PerBox({ row }: { row: BoxRow }) {
  const hasAutos = row.autosPerBox != null;
  const hasNotes = !!row.notes;
  if (!hasAutos && !hasNotes) return <Dash />;
  return (
    <span style={{ color: "var(--brand-ink-soft)" }}>
      {hasAutos && (
        <span>
          {row.autosPerBox} auto{row.autosPerBox !== 1 ? "s" : ""}/box
        </span>
      )}
      {hasAutos && hasNotes && " "}
      {hasNotes && (
        <span style={{ fontStyle: "italic", color: "var(--brand-slate)" }}>{row.notes}</span>
      )}
    </span>
  );
}

interface Props {
  boxConfig: string | null;
  packOdds: string | null;
  /** Manufacturer name inferred from the set name (e.g. "Topps", "Panini"); never hardcoded. */
  manufacturer: string;
}

export function BoxConfigTable({ boxConfig, packOdds, manufacturer }: Props) {
  if (!boxConfig) return null;
  let rows: BoxRow[];
  try {
    rows = orderRows(buildBoxRows(boxConfig), packOdds);
  } catch {
    return null;
  }
  if (rows.length === 0) return null;

  // A "—" appears whenever any shown figure is unpublished, including the
  // computed Cards/box (null when either factor is null) and an empty Per box.
  const hasDash = rows.some((r) => {
    const cardsPerBox = r.cardsPerPack != null && r.packsPerBox != null ? r.cardsPerPack * r.packsPerBox : null;
    const perBoxEmpty = r.autosPerBox == null && !r.notes;
    return r.cardsPerPack == null || r.packsPerBox == null || r.boxesPerCase == null || cardsPerBox == null || perBoxEmpty;
  });
  const mfr = manufacturer || "the manufacturer";

  const headCell = "px-3 py-2.5 text-[12px] font-semibold uppercase";
  const bodyCell = "px-3 py-2.5 border-[color:var(--brand-line)] min-[1180px]:border-b";
  const headStyle: React.CSSProperties = {
    fontFamily: FONT_MONO, letterSpacing: "0.04em", color: "var(--brand-slate)",
  };

  return (
    <div>
      <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 12 }}>
        Box Configuration
      </div>
      <div style={{ background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 12, overflow: "hidden" }}>
        <table className="w-full border-collapse" style={{ fontSize: 14 }}>
          <thead>
            <tr style={{ background: "var(--brand-track)", borderBottom: "1px solid var(--brand-line)" }}>
              <th scope="col" className={`${headCell} text-left`} style={headStyle}>Format</th>
              <th scope="col" className={`${headCell} text-right`} style={headStyle}>
                <span className="min-[1180px]:hidden">Pack</span>
                <span className="hidden min-[1180px]:inline">Cards / pack</span>
              </th>
              <th scope="col" className={`${headCell} text-right`} style={headStyle}>
                <span className="min-[1180px]:hidden">Box</span>
                <span className="hidden min-[1180px]:inline">Packs / box</span>
              </th>
              <th scope="col" className={`${headCell} text-right hidden min-[1180px]:table-cell`} style={headStyle}>Cards / box</th>
              <th scope="col" className={`${headCell} text-right`} style={headStyle}>
                <span className="min-[1180px]:hidden">Case</span>
                <span className="hidden min-[1180px]:inline">Boxes / case</span>
              </th>
              <th scope="col" className={`${headCell} text-left hidden min-[1180px]:table-cell`} style={headStyle}>Per box</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => {
              const cardsPerBox = row.cardsPerPack != null && row.packsPerBox != null ? row.cardsPerPack * row.packsPerBox : null;
              return (
                <ThisRow key={row.label} row={row} cardsPerBox={cardsPerBox} bodyCell={bodyCell} />
              );
            })}
          </tbody>
        </table>
      </div>
      <p style={{ fontSize: 12, color: "var(--brand-slate)", marginTop: 8 }}>
        Cards per box is computed.{hasDash && <> “—” means {mfr} has not published that figure.</>}
      </p>
      <p className="min-[1180px]:hidden" style={{ fontSize: 12, color: "var(--brand-slate)", marginTop: 4 }}>
        Pack = cards per pack · Box = packs per box · Case = boxes per case
      </p>
    </div>
  );
}

// One format: the data row (Per box is its 6th cell on desktop only) followed by
// a phone-only full-width row carrying the Per box text. Both live in the same
// <table>; `hidden` (display:none) keeps the off-breakpoint copy out of the
// accessibility tree, so a screen reader reads one table with no duplication.
function ThisRow({ row, cardsPerBox, bodyCell }: { row: BoxRow; cardsPerBox: number | null; bodyCell: string }) {
  const mono: React.CSSProperties = { fontFamily: FONT_MONO };
  return (
    <>
      <tr>
        <th scope="row" className={`${bodyCell} text-left`} style={{ fontFamily: FONT_DISPLAY, fontWeight: 600, color: "var(--brand-ink)" }}>
          {row.label}
        </th>
        <td className={`${bodyCell} text-right`} style={mono}><Num value={row.cardsPerPack} /></td>
        <td className={`${bodyCell} text-right`} style={mono}><Num value={row.packsPerBox} /></td>
        <td className={`${bodyCell} text-right hidden min-[1180px]:table-cell`} style={mono}><Num value={cardsPerBox} muted /></td>
        <td className={`${bodyCell} text-right`} style={mono}><Num value={row.boxesPerCase} /></td>
        <td className={`${bodyCell} text-left hidden min-[1180px]:table-cell`}><PerBox row={row} /></td>
      </tr>
      <tr className="min-[1180px]:hidden">
        <td colSpan={4} className="px-3 pb-2.5 border-b border-[color:var(--brand-line)]" style={{ fontSize: 12, color: "var(--brand-slate)" }}>
          <PerBox row={row} />
        </td>
      </tr>
    </>
  );
}
