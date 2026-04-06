interface Props {
  setName: string;
  sport: string;
  tier: string;
  athleteCount: number;
}

export function SetMetadataBar({ setName, sport, tier, athleteCount }: Props) {
  return (
    <div>
      <h1 className="text-3xl font-bold" style={{ color: "var(--v2-text-primary)" }}>
        {setName}
      </h1>
      <div className="flex flex-wrap items-center gap-2 mt-3">
        <span
          className="text-base font-medium px-4 py-1 rounded-full"
          style={{ border: "1px solid var(--v2-border)", color: "var(--v2-text-primary)" }}
        >
          {sport}
        </span>
        {tier && tier !== "Standard" && (
          <span
            className="text-base font-medium px-4 py-1 rounded-full"
            style={{ background: "var(--v2-accent-light)", color: "var(--v2-accent)", border: "1px solid var(--v2-accent)" }}
          >
            {tier}
          </span>
        )}
        <span
          className="text-base font-medium px-4 py-1 rounded-full"
          style={{ border: "1px solid var(--v2-border)", color: "var(--v2-text-secondary)" }}
        >
          {athleteCount.toLocaleString()} Athletes
        </span>
      </div>
    </div>
  );
}
