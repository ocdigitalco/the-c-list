import { db, rawQuery } from "@/lib/db";
import { notFound } from "next/navigation";
import Link from "next/link";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ id: string }>;
}

export default async function PlayerPage({ params }: Props) {
  const { id } = await params;
  const playerId = parseInt(id, 10);

  const player = await db.query.players.findFirst({
    where: (t, { eq }) => eq(t.id, playerId),
    with: {
      appearances: {
        with: {
          insertSet: {
            with: {
              parallels: true,
              set: true,
            },
          },
        },
        orderBy: (t, { asc }) => [asc(t.cardNumber)],
      },
    },
  });

  if (!player) notFound();

  // Look up set slugs for all parent sets (slug not in Drizzle schema)
  const parentSetIds = [...new Set(player.appearances.map((a) => a.insertSet.setId))];
  const setSlugMap = new Map<number, string>();
  if (parentSetIds.length > 0) {
    try {
      const placeholders = parentSetIds.map(() => "?").join(",");
      const slugRows = await rawQuery.all<{ id: number; slug: string | null }>(
        `SELECT id, slug FROM sets WHERE id IN (${placeholders})`,
        ...parentSetIds
      );
      for (const row of slugRows) {
        if (row.slug) setSlugMap.set(row.id, row.slug);
      }
    } catch { /* slug column may not exist yet */ }
  }

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-[var(--brand-slate)]">
        <Link href="/checklists" className="hover:text-[var(--brand-ink-soft)] transition-colors">
          Sets
        </Link>
        <span>/</span>
        <Link href="/players" className="hover:text-[var(--brand-ink-soft)] transition-colors">
          Players
        </Link>
        <span>/</span>
        <span className="text-[var(--brand-ink-soft)]">{player.name}</span>
      </div>

      {/* Header */}
      <div className="flex items-start justify-between">
        <h1 className="text-2xl font-normal text-[var(--brand-ink)]" style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none" }}>{player.name}</h1>
        {player.appearances.some((a) => a.isRookie) && (
          <span className="text-xs font-semibold text-amber-400 bg-amber-400/10 px-2 py-1 rounded mt-1">
            Rookie
          </span>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <StatCard label="Total Cards" value={player.uniqueCards} />
        <StatCard label="Total Print Run" value={player.totalPrintRun} />
        <StatCard label="Card Types" value={player.insertSetCount} />
        <StatCard
          label="1/1s"
          value={player.oneOfOnes}
          highlight={player.oneOfOnes > 0}
        />
      </div>

      {/* Appearances */}
      <div className="space-y-4">
        <h2 className="text-sm font-medium text-[var(--brand-ink-soft)] uppercase tracking-wider">
          Card Appearances
        </h2>

        {player.appearances.map((appearance) => (
          <div
            key={appearance.id}
            className="rounded-xl border border-[var(--brand-line)] bg-[var(--brand-card)] p-5"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <Link
                  href={`/sets/${setSlugMap.get(appearance.insertSet.setId) ?? appearance.insertSet.setId}`}
                  className="font-semibold text-[var(--brand-ink)] hover:underline"
                >
                  {appearance.insertSet.name}
                </Link>
                <div className="flex items-center gap-3 mt-1 text-sm text-[var(--brand-ink-soft)]">
                  <span className="font-mono text-[var(--brand-slate)]">#{appearance.cardNumber}</span>
                  <span>{appearance.team}</span>
                  {appearance.isRookie && (
                    <span className="text-xs font-semibold text-amber-400 bg-amber-400/10 px-1.5 py-0.5 rounded">
                      Rookie
                    </span>
                  )}
                  {appearance.subsetTag && (
                    <span className="text-xs text-[var(--brand-slate)] bg-[var(--brand-track)] px-2 py-0.5 rounded">
                      {appearance.subsetTag}
                    </span>
                  )}
                </div>
              </div>
            </div>

            {appearance.insertSet.parallels.length > 0 && (
              <div className="mt-4">
                <p className="text-xs text-[var(--brand-slate)] mb-2">Available parallels</p>
                <div className="flex flex-wrap gap-2">
                  {appearance.insertSet.parallels.map((p) => (
                    <div
                      key={p.id}
                      className="flex items-center gap-1.5 bg-[var(--brand-track)] rounded px-2.5 py-1.5"
                    >
                      <span className="text-xs text-[var(--brand-ink)]">{p.name}</span>
                      {p.printRun ? (
                        <span className="text-xs text-[var(--brand-slate)] font-mono">/{p.printRun}</span>
                      ) : (
                        <span className="text-xs text-[var(--brand-slate)]">∞</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  highlight,
}: {
  label: string;
  value: number;
  highlight?: boolean;
}) {
  return (
    <div className="rounded-lg border border-[var(--brand-line)] bg-[var(--brand-card)] px-4 py-3">
      <div className={`text-2xl font-bold ${highlight ? "text-amber-400" : "text-[var(--brand-ink)]"}`}>
        {value}
      </div>
      <div className="text-xs text-[var(--brand-slate)] mt-0.5">{label}</div>
    </div>
  );
}
