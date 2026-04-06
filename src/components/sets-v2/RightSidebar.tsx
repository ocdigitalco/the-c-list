import { BreakSheetModal, type BreakSheetPlayer } from "@/components/BreakSheetModal";

interface Props {
  releaseDate: string | null;
  hasCards: boolean;
  hasNumberedParallels: boolean;
  hasBoxConfig: boolean;
  hasPackOdds: boolean;
  sampleImageUrl: string | null;
  setName: string;
  sport: string;
  league: string | null;
  breakSheetPlayers: BreakSheetPlayer[];
}

function formatDate(iso: string): string {
  const d = new Date(iso + "T00:00:00Z");
  return d.toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

function CheckRow({ label, complete, value, isLast }: { label: string; complete: boolean; value?: string; isLast?: boolean }) {
  return (
    <div
      className="flex items-center justify-between py-2.5"
      style={isLast ? undefined : { borderBottom: "1px solid var(--v2-border)" }}
    >
      <span className="text-base" style={{ color: "var(--v2-text-primary)" }}>
        {label}
      </span>
      {value ? (
        <span className="text-base font-medium" style={{ color: "var(--v2-text-primary)" }}>
          {value}
        </span>
      ) : complete ? (
        <span
          className="flex items-center justify-center w-5 h-5 rounded-full text-white"
          style={{ background: "var(--v2-success)" }}
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
        </span>
      ) : (
        <span
          className="flex items-center justify-center w-5 h-5 rounded-full"
          style={{ background: "var(--v2-badge-bg)", color: "var(--v2-text-secondary)" }}
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14" />
          </svg>
        </span>
      )}
    </div>
  );
}

export function RightSidebar({
  releaseDate,
  hasCards,
  hasNumberedParallels,
  hasBoxConfig,
  hasPackOdds,
  sampleImageUrl,
  setName,
  sport,
  league,
  breakSheetPlayers,
}: Props) {
  return (
    <div
      className="h-full overflow-y-auto p-4 space-y-6"
      style={{ background: "var(--v2-sidebar-bg)" }}
    >
      {sampleImageUrl && (
        <img src={sampleImageUrl} alt="Set sample" className="w-full rounded-lg object-cover" />
      )}
      <div>
        <h3
          className="text-base font-medium uppercase tracking-widest mb-3"
          style={{ color: "var(--v2-text-secondary)" }}
        >
          Set Details
        </h3>
        <div
          className="rounded-lg p-3"
          style={{
            background: "var(--v2-card-bg)",
            border: "1px solid var(--v2-border)",
          }}
        >
          <CheckRow
            label="Released"
            complete={!!releaseDate}
            value={releaseDate ? formatDate(releaseDate) : "TBA"}
          />
          <CheckRow label="Athlete Checklist" complete={hasCards} />
          <CheckRow label="Numbered Parallels" complete={hasNumberedParallels} />
          <CheckRow label="Box Configuration" complete={hasBoxConfig} />
          <CheckRow label="Pack Odds" complete={hasPackOdds} isLast />
        </div>
      </div>

      <BreakSheetModal setName={setName} sport={sport} league={league} players={breakSheetPlayers} />
    </div>
  );
}
