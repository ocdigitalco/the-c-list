import { db } from "@/lib/db";
import Link from "next/link";

export const dynamic = "force-dynamic";

export default async function PlayersPage() {
  const allPlayers = await db.query.players.findMany({
    orderBy: (p, { asc }) => [asc(p.name)],
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-normal text-[var(--brand-ink)]" style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none" }}>All Players</h1>
          <p className="text-[var(--brand-ink-soft)] text-sm mt-1">{allPlayers.length} players in this set</p>
        </div>
        <Link href="/checklists" className="text-sm text-[var(--brand-ink-soft)] hover:text-[var(--brand-ink)] transition-colors">
          &larr; Back to set
        </Link>
      </div>

      <div className="rounded-xl border border-[var(--brand-line)] overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--brand-line)] bg-[var(--brand-card)]">
              <th className="text-left px-4 py-3 text-[var(--brand-ink-soft)] font-medium">Player</th>
              <th className="text-right px-4 py-3 text-[var(--brand-ink-soft)] font-medium">Cards</th>
              <th className="text-right px-4 py-3 text-[var(--brand-ink-soft)] font-medium hidden sm:table-cell">
                Numbered
              </th>
              <th className="text-right px-4 py-3 text-[var(--brand-ink-soft)] font-medium hidden md:table-cell">
                Insert Sets
              </th>
              <th className="text-right px-4 py-3 text-[var(--brand-ink-soft)] font-medium hidden md:table-cell">
                1/1s
              </th>
            </tr>
          </thead>
          <tbody>
            {allPlayers.map((player, i) => (
              <tr
                key={player.id}
                className={`border-b border-[var(--brand-line)] hover:bg-[var(--brand-card)] transition-colors ${
                  i === allPlayers.length - 1 ? "border-b-0" : ""
                }`}
              >
                <td className="px-4 py-3">
                  <Link
                    href={`/players/${player.id}`}
                    className="text-[var(--brand-ink)] hover:text-[var(--brand-ink)] font-medium hover:underline"
                  >
                    {player.name}
                  </Link>
                </td>
                <td className="px-4 py-3 text-right text-[var(--brand-ink-soft)] font-mono">
                  {player.uniqueCards}
                </td>
                <td className="px-4 py-3 text-right text-[var(--brand-ink-soft)] font-mono hidden sm:table-cell">
                  {player.totalPrintRun > 0 ? player.totalPrintRun : "—"}
                </td>
                <td className="px-4 py-3 text-right text-[var(--brand-ink-soft)] hidden md:table-cell">
                  {player.insertSetCount}
                </td>
                <td className="px-4 py-3 text-right hidden md:table-cell">
                  {player.oneOfOnes > 0 ? (
                    <span className="text-[var(--brand-ok)] font-semibold">Yes</span>
                  ) : (
                    <span className="text-[var(--brand-slate)]">—</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
