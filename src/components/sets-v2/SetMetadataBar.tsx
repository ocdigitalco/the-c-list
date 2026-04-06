interface Props {
  setName: string;
  season: string;
  league: string | null;
  tier: string;
  athletes: number;
  cards: number;
  insertSetCount: number;
  parallelTypes: number;
  totalParallels: number;
  autographs: number;
  autoParallels: number;
}

function StatChip({ value, label }: { value: number; label: string }) {
  return (
    <span className="text-[13px]" style={{ color: "var(--v2-text-secondary)" }}>
      <span className="text-[14px] font-bold" style={{ color: "var(--v2-text-primary)" }}>
        {value.toLocaleString()}
      </span>{" "}
      {label}
    </span>
  );
}

export function SetMetadataBar({
  setName,
  season,
  league,
  tier,
  athletes,
  cards,
  insertSetCount,
  parallelTypes,
  totalParallels,
  autographs,
  autoParallels,
}: Props) {
  return (
    <div>
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <span className="text-[18px] font-bold" style={{ color: "var(--v2-text-primary)" }}>
          {setName}
        </span>
        <span className="text-[13px]" style={{ color: "var(--v2-text-secondary)" }}>
          {season}
        </span>
        {league && (
          <span
            className="text-[12px] font-medium px-2 py-0.5 rounded-full"
            style={{ background: "var(--v2-badge-bg)", color: "var(--v2-text-secondary)" }}
          >
            {league}
          </span>
        )}
        {tier && tier !== "Standard" && (
          <span
            className="text-[12px] font-medium px-2 py-0.5 rounded-full"
            style={{ background: "var(--v2-accent-light)", color: "var(--v2-accent)" }}
          >
            {tier}
          </span>
        )}
      </div>
      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-2">
        <StatChip value={athletes} label="athletes" />
        <StatChip value={cards} label="cards" />
        <StatChip value={insertSetCount} label="insert sets" />
        <StatChip value={parallelTypes} label="parallel types" />
        <StatChip value={totalParallels} label="total parallels" />
        <StatChip value={autographs} label="autographs" />
        <StatChip value={autoParallels} label="autograph parallels" />
      </div>
      <hr className="mt-4" style={{ borderColor: "var(--v2-border)" }} />
    </div>
  );
}
