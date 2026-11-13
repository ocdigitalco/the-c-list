import React from "react";
import styles from "./ParallelOddsTable.module.css";
import { printRunDisplay } from "./ParallelTable";
import { label as boxLabel } from "@/lib/boxLabels";
import type { ResolvedOdds } from "@/lib/athleteOddsResolver";
import { subsetChipModel, toChipRow, type HeaderChip, type RowChip } from "@/lib/athleteSubsetChips";

/** One appearance of the athlete in this subset — renders the card header. */
export interface OddsTableAppearance {
  cardNumber: string;
  team: string | null;
  isRookie: boolean;
}

/** One parallel (or the synthetic "Base") row. */
export interface OddsTableRow {
  name: string;
  printRun: number | null;
  exclusivity: string | null;
  /** Resolved odds for the active-format order, or null → "—". */
  resolved: ResolvedOdds | null;
  /** eBay affiliate URL (null when no EPN campaign configured). */
  shopUrl: string | null;
}

function displayOdds(v: string | number | null): string {
  if (v == null) return "—";
  if (typeof v === "number") return `1:${v.toLocaleString()}`;
  return String(v);
}

/** Red name only for the top chase (SuperFractor), per the approved canvas. */
function isChase(name: string): boolean {
  return /superfractor/i.test(name);
}

function headerTitle(h: HeaderChip): string {
  const name = h.text.replace(/ (only|odds)$/, "");
  return h.dark
    ? `Odds shown for ${name} boxes unless a row says otherwise`
    : `Every parallel in this subset is found only in ${name} boxes`;
}

function rowChipTitle(c: RowChip): string {
  if (c.text === "No published odds") return "No published pack odds for this parallel";
  const name = c.text.replace(/ only$/, "");
  // Dashed chips come from parallels.exclusivity (a place, not a box format).
  return c.dashed ? `Found only in ${name}` : `Found only in ${name} boxes`;
}

const ExternalLinkIcon = ({ size }: { size: number }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" aria-hidden="true">
    <path d="M4 12L12 4M6 4h6v6" fill="none" stroke="currentColor" strokeWidth={1.6} />
  </svg>
);

/**
 * Per-subset parallel odds table for the set-scoped athlete page. One grid row
 * per parallel; the resolved box format is shown once in the subset header and
 * repeated on a row only when that row's figure came from a different format.
 * Adapts to its container width (see the CSS module), not the viewport.
 */
export function ParallelOddsTable({
  subsetName, cardsCount, parallelsCount, athleteName,
  appearances, rows, selectedFormatKey, flat = false, showEbay = true,
}: {
  subsetName: string;
  cardsCount: number;
  parallelsCount: number;
  athleteName: string;
  appearances: OddsTableAppearance[];
  rows: OddsTableRow[];
  selectedFormatKey: string | null;
  flat?: boolean;
  showEbay?: boolean;
}) {
  const model = subsetChipModel(
    rows.map((r) => toChipRow(r.resolved, r.exclusivity)),
    selectedFormatKey,
    boxLabel,
    { flat },
  );

  return (
    <section className={`${styles.wrap}${showEbay ? "" : ` ${styles.noEbay}`}`}>
      <div className={styles.shead}>
        <div className={styles.sheadTop}>
          <h3 className={styles.title}>{subsetName}</h3>
          <span className={styles.count}>
            {cardsCount} card{cardsCount !== 1 ? "s" : ""}
            {parallelsCount > 0 ? ` · ${parallelsCount} parallel${parallelsCount !== 1 ? "s" : ""}` : ""}
          </span>
        </div>
        {model.header && (
          <span
            className={`${styles.chip}${model.header.dark ? ` ${styles.chipDark}` : ""}`}
            style={{ alignSelf: "flex-start" }}
            title={headerTitle(model.header)}
          >
            {model.header.text}
          </span>
        )}
      </div>

      <div className={styles.card}>
        {appearances.map((a, i) => (
          <div key={`${a.cardNumber}-${i}`} className={styles.cardHead}>
            <div className={styles.cardHeadRow}>
              <span className={styles.cardNum}>#{a.cardNumber}</span>
              <span className={styles.cardName}>{athleteName}</span>
              {a.isRookie && <span className={styles.rc} title="Rookie Card">RC</span>}
              {a.team && <span className={styles.team}>{a.team}</span>}
            </div>
          </div>
        ))}

        {/* Column headers — phone + desktop variants toggled by the container query. */}
        <div className={styles.headPhone}>
          <span className={styles.hcell}>Parallel · Print run · Found in</span>
          <span className={`${styles.hcell} ${styles.right}`}>Pack odds</span>
          <span className={styles.hEbay} aria-hidden="true" />
        </div>
        <div className={styles.headDesktop}>
          <span className={styles.hcell}>Parallel</span>
          <span className={styles.hcell}>Found in</span>
          <span className={`${styles.hcell} ${styles.right}`}>Print run</span>
          <span className={`${styles.hcell} ${styles.right}`}>Pack odds</span>
          <span className={`${styles.hcell} ${styles.hEbay}`}>eBay</span>
        </div>

        {rows.map((r, i) => {
          const chip = model.rows[i];
          const oneOfOne = r.printRun === 1;
          // Red parallel name on every 1/1 row (as on the set page), plus the
          // SuperFractor chase even when its print run isn't carried.
          const nameRed = oneOfOne || isChase(r.name);
          const prText = printRunDisplay(r.printRun);
          const oddsText = displayOdds(r.resolved ? r.resolved.value : null);
          const noOdds = r.resolved == null;

          return (
            <div key={`${r.name}-${i}`} className={styles.row}>
              {/* Col 1: parallel name (+ phone meta line) */}
              <div>
                <span className={`${styles.pname}${nameRed ? ` ${styles.pnameOne}` : ""}`}>{r.name}</span>
                <div className={styles.meta}>
                  <span className={oneOfOne ? styles.metaOne : undefined}>{prText}</span>
                  {chip && (
                    <>
                      <span className={styles.metaDot}>·</span>
                      <span>{chip.text}</span>
                    </>
                  )}
                </div>
              </div>

              {/* Col 2 (desktop): Found in */}
              <div className={styles.cFound}>
                {chip && (
                  <span
                    className={`${styles.chip}${chip.dashed ? ` ${styles.chipDashed}` : ""}`}
                    title={rowChipTitle(chip)}
                  >
                    {chip.text}
                  </span>
                )}
              </div>

              {/* Col 3 (desktop): Print run */}
              <div className={`${styles.cPr} ${styles.pr}${oneOfOne ? ` ${styles.prOne}` : ""}`}>{prText}</div>

              {/* Pack odds */}
              <div className={`${styles.num}${noOdds ? ` ${styles.numDash}` : ""}`}>{oddsText}</div>

              {/* eBay */}
              {showEbay && (
                <div className={styles.cEbay}>
                  {r.shopUrl && (
                    <>
                      <a className={styles.ebayText} href={r.shopUrl} target="_blank" rel="sponsored noopener" aria-label={`Find ${r.name} on eBay`}>
                        Find on eBay <ExternalLinkIcon size={12} />
                      </a>
                      <a className={styles.ebayIcon} href={r.shopUrl} target="_blank" rel="sponsored noopener" aria-label={`Find ${r.name} on eBay`}>
                        <ExternalLinkIcon size={16} />
                      </a>
                    </>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
