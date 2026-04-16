interface SetInfoData {
  name: string;
  sport: string;
  league: string | null;
  season: string;
  tier: string;
  sampleImageUrl: string | null;
  cardCount: number;
  insertSetCount: number;
  athleteCount: number;
  boxTypeCount: number;
}

const PILL_COLORS: Record<string, string> = {
  sport: "border-blue-500/40 bg-blue-500/10 text-blue-400",
  league: "border-pink-500/40 bg-pink-500/10 text-pink-400",
  season: "border-green-500/40 bg-green-500/10 text-green-400",
  tier: "border-amber-500/40 bg-amber-500/10 text-amber-400",
};

export function SetInfoCard({ data }: { data: SetInfoData }) {
  const pills = [
    { key: "sport", value: data.sport },
    ...(data.league ? [{ key: "league", value: data.league }] : []),
    { key: "season", value: data.season },
    { key: "tier", value: data.tier },
  ];

  const stats = [
    { label: "Cards", value: data.cardCount },
    { label: "Card Types", value: data.insertSetCount },
    { label: "Athletes", value: data.athleteCount },
    { label: "Box Types", value: data.boxTypeCount },
  ];

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden mb-6">
      <div className="flex flex-col sm:flex-row gap-4 p-5">
        {data.sampleImageUrl && (
          <div className="shrink-0 w-full sm:w-28 aspect-[4/3] sm:aspect-square rounded-lg overflow-hidden border border-zinc-800">
            <img
              src={data.sampleImageUrl}
              alt={data.name}
              className="w-full h-full object-cover"
            />
          </div>
        )}
        <div className="flex-1 min-w-0">
          <p className="text-lg font-bold text-white leading-tight">
            {data.name}
          </p>
          <div className="flex flex-wrap gap-1.5 mt-2">
            {pills.map((p) => (
              <span
                key={p.key}
                className={`text-[14px] font-medium px-2.5 py-0.5 rounded-full border ${PILL_COLORS[p.key]}`}
              >
                {p.value}
              </span>
            ))}
          </div>
        </div>
      </div>
      <div className="grid grid-cols-4 border-t border-zinc-800">
        {stats.map((s) => (
          <div key={s.label} className="px-4 py-3 text-center">
            <p className="text-lg font-bold text-white tabular-nums">
              {s.value.toLocaleString()}
            </p>
            <p className="text-[11px] text-zinc-500 uppercase tracking-wide">
              {s.label}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
