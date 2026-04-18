"use client";

import { useState } from "react";
import type { BoxConfigSingle, BoxConfigMulti } from "./types";
import { normalizeOddsObj, denomToDisplay } from "@/lib/parseOdds";

// ─── Types ────────────────────────────────────────────────���───────────────────

type OddsCategory = "Autographs" | "Base Parallels" | "Inserts";

interface OddsRow {
  key: string;
  denom: number;
  category: OddsCategory;
}

interface OddsFormat {
  label: string;
  rows: OddsRow[];
  packsPerBox: number;
}

// ─── Helpers ───────────��──────────────────────────────────────��───────────────

function categorize(key: string): OddsCategory {
  const lower = key.toLowerCase();
  if (lower.includes("auto") || lower.includes("autograph") || lower.includes("signature"))
    return "Autographs";
  if (lower.startsWith("base")) return "Base Parallels";
  return "Inserts";
}

const BOX_LABEL_MAP: Record<string, string> = {
  hobby: "Hobby",
  jumbo: "Jumbo",
  mega: "Mega",
  blaster: "Blaster",
  value: "Value",
  fat_pack: "Fat Pack",
  hanger: "Hanger",
  breakers_delight: "Breaker's Delight",
  first_day_issue: "First Day Issue",
  breaker: "Breaker",
  hobby_hybrid: "Hobby Hybrid",
  sapphire: "Sapphire",
  hongbao: "Hongbao",
  logofractor: "Logofractor",
  ffnyc: "FFNYC",
  fdi: "First Day Issue",
  // Retail exclusive variants (SE/EA/CEE) map to their base box type
  value_se: "Value",
  value_ea: "Value",
  value_cee: "Value",
  mega_se: "Mega",
  mega_ea: "Mega",
  mega_cee: "Mega",
  hanger_se: "Hanger",
  hanger_ea: "Hanger",
  hanger_cee: "Hanger",
};

function formatBoxLabel(key: string): string {
  return BOX_LABEL_MAP[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

// ─── Sub-components ────────────────��──────────────────────────────────────────

const CATEGORY_ORDER: OddsCategory[] = ["Base Parallels", "Inserts", "Autographs"];

function isSuperfractor(key: string): boolean {
  return key.toLowerCase().includes("superfractor");
}

function OddsTableSection({
  title,
  rows,
  packsPerBox,
  accent,
}: {
  title: string;
  rows: OddsRow[];
  packsPerBox: number;
  accent?: boolean;
}) {
  if (rows.length === 0) return null;
  return (
    <div>
      <h3
        className="text-base font-medium uppercase tracking-widest mb-2"
        style={{ color: accent ? "#d97706" : "var(--v2-text-secondary)" }}
      >
        {title}
      </h3>
      <div className="rounded-lg overflow-hidden" style={{ border: `1px solid ${accent ? "#d9770633" : "var(--v2-border)"}` }}>
        <table className="w-full">
          <thead>
            <tr style={{ background: "var(--v2-card-bg)" }}>
              <th
                className="text-left text-base font-medium uppercase tracking-wide px-4 py-2.5"
                style={{ color: "var(--v2-text-secondary)", borderBottom: "1px solid var(--v2-border)" }}
              >
                Parallel / Insert
              </th>
              <th
                className="text-right text-base font-medium uppercase tracking-wide px-4 py-2.5"
                style={{ color: "var(--v2-text-secondary)", borderBottom: "1px solid var(--v2-border)" }}
              >
                Pack Odds
              </th>
              <th
                className="text-right text-base font-medium uppercase tracking-wide px-4 py-2.5 hidden sm:table-cell"
                style={{ color: "var(--v2-text-secondary)", borderBottom: "1px solid var(--v2-border)" }}
              >
                Per Box ({packsPerBox} packs)
              </th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr
                key={row.key}
                className="transition-colors"
                style={{
                  background: i % 2 === 1 ? "var(--v2-row-alt)" : "var(--v2-card-bg)",
                  borderBottom: "1px solid var(--v2-border)",
                }}
              >
                <td className="px-4 py-2.5 text-base" style={{ color: "var(--v2-text-primary)" }}>
                  {row.key}
                </td>
                <td
                  className="px-4 py-2.5 text-base font-mono tabular-nums text-right"
                  style={{ color: "var(--v2-text-secondary)" }}
                >
                  {denomToDisplay(row.denom)}
                </td>
                <td
                  className="px-4 py-2.5 text-base tabular-nums text-right hidden sm:table-cell"
                  style={{ color: "var(--v2-text-secondary)" }}
                >
                  {packsPerBox / row.denom >= 1
                    ? `~${(packsPerBox / row.denom).toFixed(1)}×`
                    : `1 in ~${(row.denom / packsPerBox).toFixed(1)} boxes`}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function OddsTable({ rows, packsPerBox }: { rows: OddsRow[]; packsPerBox: number }) {
  const regularRows = rows.filter((r) => !isSuperfractor(r.key));
  const superfractorRows = rows.filter((r) => isSuperfractor(r.key)).sort((a, b) => a.denom - b.denom);

  const grouped = CATEGORY_ORDER.reduce(
    (acc, cat) => {
      acc[cat] = regularRows.filter((r) => r.category === cat).sort((a, b) => a.denom - b.denom);
      return acc;
    },
    {} as Record<OddsCategory, OddsRow[]>
  );

  return (
    <div className="space-y-5">
      {CATEGORY_ORDER.map((cat) => (
        <OddsTableSection
          key={cat}
          title={cat}
          rows={grouped[cat]}
          packsPerBox={packsPerBox}
        />
      ))}
      {superfractorRows.length > 0 && (
        <OddsTableSection
          title="Superfractors (1/1)"
          rows={superfractorRows}
          packsPerBox={packsPerBox}
          accent
        />
      )}
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

interface Props {
  boxConfig: string | null;
  packOdds: string | null;
}

export function PackOddsInline({ boxConfig, packOdds }: Props) {
  const [activeIdx, setActiveIdx] = useState(0);

  if (!packOdds) {
    return (
      <div
        className="rounded-lg px-5 py-8 text-center text-base italic"
        style={{ background: "var(--v2-card-bg)", border: "1px solid var(--v2-border)", color: "var(--v2-text-secondary)" }}
      >
        Pack odds coming soon
      </div>
    );
  }

  // Parse box config for packs_per_box lookup
  const boxFormats: { label: string; packsPerBox: number }[] = [];
  if (boxConfig) {
    const rawBox = JSON.parse(boxConfig) as BoxConfigSingle | BoxConfigMulti;
    if (isMultiConfig(rawBox)) {
      for (const [key, cfg] of Object.entries(rawBox)) {
        boxFormats.push({ label: formatBoxLabel(key), packsPerBox: cfg.packs_per_box ?? 12 });
      }
    } else {
      boxFormats.push({ label: "Box", packsPerBox: (rawBox as BoxConfigSingle).packs_per_box ?? 12 });
    }
  }

  function packsPerBoxFor(label: string): number {
    const fmt = boxFormats.find((f) => f.label.toLowerCase() === label.toLowerCase());
    return fmt?.packsPerBox ?? 12;
  }

  function buildOddsRows(data: Record<string, number>): OddsRow[] {
    return Object.entries(data).map(([key, denom]) => ({ key, denom, category: categorize(key) }));
  }

  // Build odds formats
  const rawOdds = JSON.parse(packOdds);
  const firstVal = Object.values(rawOdds)[0];
  const isNestedOdds = firstVal !== null && typeof firstVal === "object";

  const oddsFormats: OddsFormat[] = [];
  if (isNestedOdds) {
    for (const [key, data] of Object.entries(rawOdds as Record<string, Record<string, unknown>>)) {
      const label = formatBoxLabel(key);
      // First key for a given label wins (e.g. value before value_se)
      if (!oddsFormats.some((f) => f.label === label)) {
        oddsFormats.push({ label, rows: buildOddsRows(normalizeOddsObj(data)), packsPerBox: packsPerBoxFor(label) });
      }
    }
  } else {
    const label = boxFormats.length === 1 ? boxFormats[0].label : "Box";
    oddsFormats.push({ label, rows: buildOddsRows(normalizeOddsObj(rawOdds as Record<string, unknown>)), packsPerBox: packsPerBoxFor(label) });
  }

  const active = oddsFormats[activeIdx] ?? oddsFormats[0];

  return (
    <div className="space-y-3">
      {oddsFormats.length > 1 && (
        <div
          className="flex gap-1 rounded-lg p-0.5 w-fit max-w-full overflow-x-auto"
          style={{ background: "var(--v2-badge-bg)" }}
        >
          {oddsFormats.map((f, i) => (
            <button
              key={f.label}
              onClick={() => setActiveIdx(i)}
              className="px-4 text-base py-1.5 rounded-md font-medium transition-colors"
              style={{
                background: i === activeIdx ? "var(--v2-accent)" : "transparent",
                color: i === activeIdx ? "#FFFFFF" : "var(--v2-text-secondary)",
              }}
            >
              {f.label}
            </button>
          ))}
        </div>
      )}
      <OddsTable rows={active.rows} packsPerBox={active.packsPerBox} />
      <p className="text-base leading-relaxed" style={{ color: "var(--v2-text-secondary)" }}>
        Odds are per-pack as reported by the manufacturer. Numbered parallels are serialized to the
        print run shown on the card.
      </p>
    </div>
  );
}
