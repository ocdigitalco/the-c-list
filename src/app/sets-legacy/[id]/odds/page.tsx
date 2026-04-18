import { db } from "@/lib/db";
import { notFound } from "next/navigation";
import Link from "next/link";
import { OddsTabView } from "./OddsTabView";
import { normalizeOddsObj, denomToDisplay } from "@/lib/parseOdds";

export const dynamic = "force-dynamic";

// ─── Types ────────────────────────────────────────────────────────────────────

type BoxFormatSingle = {
  cards_per_pack?: number;
  packs_per_box?: number;
  boxes_per_case?: number;
  [key: string]: number | undefined;
};
type BoxFormatMulti = Record<string, BoxFormatSingle>;

type OddsCategory = "Autographs" | "Base Parallels" | "Inserts";

interface OddsRow {
  key: string;
  denom: number;
  category: OddsCategory;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function categorize(key: string): OddsCategory {
  const lower = key.toLowerCase();
  if (
    lower.includes("auto") ||
    lower.includes("autograph") ||
    lower.includes("signature")
  )
    return "Autographs";
  if (lower.startsWith("base")) return "Base Parallels";
  return "Inserts";
}

function formatFieldName(key: string): string {
  return key
    .replace(/_/g, " ")
    .replace(/\bper\b/, "/")
    .replace(/\b\w/g, (c) => c.toUpperCase());
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

// ─── Sub-components ───────────────────────────────────────────────────────────

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-lg border border-zinc-700/60 bg-zinc-800/50 px-4 py-3">
      <p className="text-xs font-medium text-zinc-500 mb-0.5">{label}</p>
      <p className="text-sm font-bold text-white tabular-nums">{value}</p>
    </div>
  );
}

function BoxConfigCards({ config }: { config: BoxFormatSingle }) {
  const SKIP = new Set(["cards_per_pack", "packs_per_box", "boxes_per_case"]);
  const extras = Object.entries(config).filter(
    ([k, v]) => !SKIP.has(k) && v != null
  );
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
      {config.cards_per_pack != null && (
        <StatCard label="Cards / Pack" value={config.cards_per_pack} />
      )}
      {config.packs_per_box != null && (
        <StatCard label="Packs / Box" value={config.packs_per_box} />
      )}
      {config.boxes_per_case != null && (
        <StatCard label="Boxes / Case" value={config.boxes_per_case} />
      )}
      {config.packs_per_box != null && config.boxes_per_case != null && (
        <StatCard
          label="Packs / Case"
          value={(config.packs_per_box * config.boxes_per_case).toLocaleString()}
        />
      )}
      {extras.map(([k, v]) => (
        <StatCard key={k} label={formatFieldName(k)} value={v!} />
      ))}
    </div>
  );
}

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
      <h3 className="text-xs font-semibold uppercase tracking-widest mb-2" style={{ color: accent ? "#d97706" : undefined }}>
        {!accent && <span className="text-zinc-400">{title}</span>}
        {accent && title}
      </h3>
      <div className="rounded-xl border overflow-hidden" style={{ borderColor: accent ? "#d9770633" : undefined }}>
        <table className="w-full">
          <thead>
            <tr className="border-b border-zinc-800 bg-zinc-900/60">
              <th className="text-left text-xs font-semibold text-zinc-600 uppercase tracking-wider px-4 py-2.5">
                Parallel / Insert
              </th>
              <th className="text-right text-xs font-semibold text-zinc-600 uppercase tracking-wider px-4 py-2.5">
                Pack Odds
              </th>
              <th className="text-right text-xs font-semibold text-zinc-600 uppercase tracking-wider px-4 py-2.5 hidden sm:table-cell">
                Per Box ({packsPerBox} packs)
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800/60">
            {rows.map((row) => (
              <tr key={row.key} className="bg-zinc-900 hover:bg-zinc-800/40 transition-colors">
                <td className="px-4 py-2.5 text-sm text-zinc-300">{row.key}</td>
                <td className="px-4 py-2.5 text-sm font-mono tabular-nums text-zinc-400 text-right">
                  {denomToDisplay(row.denom)}
                </td>
                <td className="px-4 py-2.5 text-xs text-zinc-600 text-right tabular-nums hidden sm:table-cell">
                  {(packsPerBox / row.denom) >= 1
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
  const CATEGORY_ORDER: OddsCategory[] = ["Base Parallels", "Inserts", "Autographs"];

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
    <div className="space-y-6">
      {CATEGORY_ORDER.map((cat) => (
        <OddsTableSection key={cat} title={cat} rows={grouped[cat]} packsPerBox={packsPerBox} />
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

// ─── Page ─────────────────────────────────────────────────────────────────────

export default async function OddsPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const setId = parseInt(id, 10);
  if (isNaN(setId)) notFound();

  const setRow = await db.query.sets.findFirst({
    where: (t, { eq }) => eq(t.id, setId),
  });
  if (!setRow) notFound();

  const hasBoxConfig = !!setRow.boxConfig;
  const hasPackOdds = !!setRow.packOdds;

  const rawBoxConfig = hasBoxConfig
    ? (JSON.parse(setRow.boxConfig!) as BoxFormatSingle | BoxFormatMulti)
    : null;

  // Detect multi-format: any value that is an object with box config fields
  function isMultiConfig(cfg: BoxFormatSingle | BoxFormatMulti): cfg is BoxFormatMulti {
    const first = Object.values(cfg)[0];
    return first !== null && typeof first === "object";
  }

  const boxFormats: { label: string; config: BoxFormatSingle }[] = [];
  if (rawBoxConfig) {
    if (isMultiConfig(rawBoxConfig)) {
      for (const [key, config] of Object.entries(rawBoxConfig)) {
        boxFormats.push({ label: formatBoxLabel(key), config });
      }
    } else {
      boxFormats.push({ label: "Box", config: rawBoxConfig as BoxFormatSingle });
    }
  }

  // Pack odds: detect flat vs nested { hobby: {...}, jumbo: {...} }
  interface OddsFormat {
    label: string;
    rows: OddsRow[];
    packsPerBox: number;
  }

  function packsPerBoxFor(label: string): number {
    const fmt = boxFormats.find((f) => f.label.toLowerCase() === label.toLowerCase());
    return fmt?.config.packs_per_box ?? 12;
  }

  function buildOddsRows(data: Record<string, number>): OddsRow[] {
    return Object.entries(data).map(([key, denom]) => ({ key, denom, category: categorize(key) }));
  }

  const oddsFormats: OddsFormat[] = [];
  if (hasPackOdds) {
    const rawOdds = JSON.parse(setRow.packOdds!);
    const firstVal = Object.values(rawOdds)[0];
    const isNestedOdds = firstVal !== null && typeof firstVal === "object";

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
  }

  return (
    <div className="h-full overflow-y-auto bg-zinc-950">
      <div className="max-w-4xl mx-auto px-5 py-8 space-y-8">
        {/* Breadcrumb */}
        <div className="flex items-center gap-1.5 text-xs">
          <Link
            href={`/checklists?sport=${encodeURIComponent(setRow.sport)}`}
            className="text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            {setRow.sport}
          </Link>
          <span className="text-zinc-700">/</span>
          <Link
            href={`/sets-legacy/${setId}`}
            className="text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            {setRow.name}
          </Link>
          <span className="text-zinc-700">/</span>
          <span className="text-zinc-400">Pack Odds</span>
        </div>

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">{setRow.name}</h1>
          <p className="text-sm text-zinc-500 mt-1">Pack odds &amp; box configuration</p>
        </div>

        {/* Box Config */}
        {hasBoxConfig ? (
          <section className="space-y-4">
            <h2 className="text-xs font-semibold text-zinc-400 uppercase tracking-widest">
              Box Configuration
            </h2>
            {boxFormats.length === 1 ? (
              <BoxConfigCards config={boxFormats[0].config} />
            ) : (
              <div className="space-y-5">
                {boxFormats.map(({ label, config }) => (
                  <div key={label}>
                    <p className="text-sm font-semibold text-zinc-400 mb-2">{label}</p>
                    <BoxConfigCards config={config} />
                  </div>
                ))}
              </div>
            )}
          </section>
        ) : (
          <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 px-5 py-4">
            <p className="text-sm font-semibold text-amber-400">Box configuration not available</p>
            <p className="text-xs text-amber-400/60 mt-0.5">
              Box configuration data hasn&apos;t been added for this set yet.
            </p>
          </div>
        )}

        {/* Pack Odds */}
        {hasPackOdds && oddsFormats.length > 0 ? (
          <section className="space-y-4">
            <h2 className="text-xs font-semibold text-zinc-400 uppercase tracking-widest">
              Pack Odds
            </h2>
            {oddsFormats.length > 1 ? (
              <OddsTabView formats={oddsFormats} />
            ) : (
              <OddsTable rows={oddsFormats[0].rows} packsPerBox={oddsFormats[0].packsPerBox} />
            )}
            <p className="text-xs text-zinc-700 leading-relaxed">
              Odds are per-pack as reported by the manufacturer. Numbered parallels are serialized
              to the print run shown on the card.
            </p>
          </section>
        ) : (
          <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 px-5 py-4">
            <p className="text-sm font-semibold text-amber-400">Pack odds not available</p>
            <p className="text-xs text-amber-400/60 mt-0.5">
              Official pack odds haven&apos;t been added for this set yet. The Break Hit Calculator
              requires this data to compute probabilities.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
