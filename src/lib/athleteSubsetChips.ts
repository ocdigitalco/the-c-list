/**
 * Chip model for one subset card on the set-scoped athlete page's parallel table.
 * Pure and side-effect-free so the header/row chip rules stay unit-testable.
 *
 * Header chip: if every row that resolved a figure shares ONE named format, the
 * header reads "<Format> only" (muted) and no row carries a chip. Otherwise the
 * header shows the currently-selected format as "<Format> odds" (dark) and only
 * the rows whose figure came from a different format carry a "<Format> only"
 * chip. Flat (unnamed) pack odds render no chips at all. A row with no figure in
 * any format shows a dashed "No published odds" chip — or "<Exclusivity> only"
 * when the parallel is format-exclusive, since that is the one thing we do know.
 */
import type { ResolvedOdds } from "./athleteOddsResolver";

/** Format key buildOrderedFormats uses for non-nested (flat) pack_odds. */
export const FLAT_FORMAT_KEY = "__flat__";

export interface ChipRow {
  /** Resolved format key, FLAT_FORMAT_KEY for flat odds, or null with no figure anywhere. */
  formatKey: string | null;
  /** parallels.exclusivity — the keyless "Found in" fallback. */
  exclusivity?: string | null;
}

export interface HeaderChip {
  text: string;
  /** true → dark (ink) selected-format chip; false → muted "only" chip. */
  dark: boolean;
}
export interface RowChip {
  text: string;
  /** true → dashed, transparent "no odds" chip; false → muted solid "only" chip. */
  dashed: boolean;
}
export interface SubsetChipModel {
  header: HeaderChip | null;
  /** One entry per input row (same order); null → no chip on that row. */
  rows: (RowChip | null)[];
}

/** Map a ResolvedOdds-or-null + exclusivity into the ChipRow the model consumes. */
export function toChipRow(resolved: ResolvedOdds | null, exclusivity: string | null): ChipRow {
  return { formatKey: resolved ? resolved.formatKey : null, exclusivity };
}

export function subsetChipModel(
  rows: ChipRow[],
  selectedFormatKey: string | null,
  label: (key: string) => string,
  opts: { flat?: boolean } = {},
): SubsetChipModel {
  // Flat (unnamed) odds carry no format identity → no chips of any kind.
  if (opts.flat) return { header: null, rows: rows.map(() => null) };

  const figured = rows.filter((r): r is ChipRow & { formatKey: string } => r.formatKey != null);
  const distinct = new Set(figured.map((r) => r.formatKey));
  const soleNamed =
    figured.length > 0 && distinct.size === 1 && !distinct.has(FLAT_FORMAT_KEY)
      ? [...distinct][0]
      : null;

  // The format the header represents: the single shared named format when every
  // figured row agrees on it, otherwise the selected chip's format.
  const headerFormatKey = soleNamed ?? selectedFormatKey;

  let header: HeaderChip | null;
  if (soleNamed) {
    header = { text: `${label(soleNamed)} only`, dark: false };
  } else if (selectedFormatKey && selectedFormatKey !== FLAT_FORMAT_KEY) {
    header = { text: `${label(selectedFormatKey)} odds`, dark: true };
  } else {
    header = null;
  }

  const rowChips = rows.map((r): RowChip | null => {
    if (r.formatKey == null) {
      return { text: r.exclusivity ? `${r.exclusivity} only` : "No published odds", dashed: true };
    }
    if (r.formatKey !== FLAT_FORMAT_KEY && r.formatKey !== headerFormatKey) {
      return { text: `${label(r.formatKey)} only`, dashed: false };
    }
    return null;
  });

  return { header, rows: rowChips };
}
