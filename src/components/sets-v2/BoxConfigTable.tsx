import type { BoxConfigSingle, BoxConfigMulti } from "./types";

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
};

function formatBoxLabel(key: string): string {
  return BOX_LABEL_MAP[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

function getAutosPerBox(fmt: BoxConfigSingle): number | null {
  return (
    fmt.autos_per_box ??
    fmt.autos_or_memorabilia_per_box ??
    fmt.autos_or_relics_per_box ??
    fmt.autos_or_auto_relics_per_box ??
    null
  );
}

interface RowData {
  label: string;
  cardsPerPack: number | null;
  packsPerBox: number | null;
  boxesPerCase: number | null;
  packsPerCase: string;
  autosPerBox: number | null;
  notes?: string;
}

function buildRows(boxConfig: string): RowData[] {
  const raw = JSON.parse(boxConfig) as BoxConfigSingle | BoxConfigMulti;
  if (isMultiConfig(raw)) {
    return Object.entries(raw).map(([key, fmt]) => {
      const ppb = fmt.packs_per_box ?? null;
      const bpc = fmt.boxes_per_case ?? null;
      return {
        label: formatBoxLabel(key),
        cardsPerPack: fmt.cards_per_pack ?? null,
        packsPerBox: ppb,
        boxesPerCase: bpc,
        packsPerCase: ppb != null && bpc != null ? (ppb * bpc).toLocaleString() : "—",
        autosPerBox: getAutosPerBox(fmt),
        notes: fmt.notes ?? fmt.note,
      };
    });
  }
  const fmt = raw as BoxConfigSingle;
  const ppb = fmt.packs_per_box ?? null;
  const bpc = fmt.boxes_per_case ?? null;
  return [
    {
      label: "Hobby",
      cardsPerPack: fmt.cards_per_pack ?? null,
      packsPerBox: ppb,
      boxesPerCase: bpc,
      packsPerCase: ppb != null && bpc != null ? (ppb * bpc).toLocaleString() : "—",
      autosPerBox: getAutosPerBox(fmt),
      notes: fmt.notes ?? fmt.note,
    },
  ];
}

interface Props {
  boxConfig: string | null;
}

export function BoxConfigTable({ boxConfig }: Props) {
  if (!boxConfig) {
    return (
      <div
        className="rounded-lg px-5 py-8 text-center text-sm italic"
        style={{ background: "var(--v2-card-bg)", border: "1px solid var(--v2-border)", color: "var(--v2-text-secondary)" }}
      >
        Box configuration coming soon
      </div>
    );
  }

  const rows = buildRows(boxConfig);

  return (
    <div
      className="rounded-lg overflow-hidden"
      style={{ border: "1px solid var(--v2-border)" }}
    >
      <table className="w-full text-sm">
        <thead>
          <tr style={{ background: "var(--v2-card-bg)" }}>
            {["Box Type", "Cards/Pack", "Packs/Box", "Boxes/Case", "Packs/Case", "Autos/Box"].map(
              (h) => (
                <th
                  key={h}
                  className="text-left text-[12px] font-medium uppercase tracking-wide px-4 py-2.5"
                  style={{ color: "var(--v2-text-secondary)", borderBottom: "1px solid var(--v2-border)" }}
                >
                  {h}
                </th>
              )
            )}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={row.label}>
              <td
                className="px-4 py-2.5 font-medium"
                style={{
                  color: "var(--v2-text-primary)",
                  background: i % 2 === 1 ? "var(--v2-row-alt)" : "var(--v2-card-bg)",
                  borderBottom: row.notes ? "none" : "1px solid var(--v2-border)",
                }}
              >
                {row.label}
              </td>
              {[row.cardsPerPack, row.packsPerBox, row.boxesPerCase].map((val, j) => (
                <td
                  key={j}
                  className="px-4 py-2.5 tabular-nums"
                  style={{
                    color: "var(--v2-text-primary)",
                    background: i % 2 === 1 ? "var(--v2-row-alt)" : "var(--v2-card-bg)",
                    borderBottom: row.notes ? "none" : "1px solid var(--v2-border)",
                  }}
                >
                  {val ?? "—"}
                </td>
              ))}
              <td
                className="px-4 py-2.5 tabular-nums"
                style={{
                  color: "var(--v2-text-primary)",
                  background: i % 2 === 1 ? "var(--v2-row-alt)" : "var(--v2-card-bg)",
                  borderBottom: row.notes ? "none" : "1px solid var(--v2-border)",
                }}
              >
                {row.packsPerCase}
              </td>
              <td
                className="px-4 py-2.5 tabular-nums"
                style={{
                  color: "var(--v2-text-primary)",
                  background: i % 2 === 1 ? "var(--v2-row-alt)" : "var(--v2-card-bg)",
                  borderBottom: row.notes ? "none" : "1px solid var(--v2-border)",
                }}
              >
                {row.autosPerBox ?? "—"}
              </td>
              {row.notes && (
                <>
                  {/* Notes row spans full width — rendered as next <tr> */}
                </>
              )}
            </tr>
          ))}
          {rows
            .filter((r) => r.notes)
            .map((row) => (
              <tr key={`${row.label}-notes`}>
                <td
                  colSpan={6}
                  className="px-4 py-1.5 text-xs italic"
                  style={{
                    color: "var(--v2-text-secondary)",
                    background: "var(--v2-card-bg)",
                    borderBottom: "1px solid var(--v2-border)",
                  }}
                >
                  {row.notes}
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}
