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
          <h1 className="text-2xl font-bold text-white">All Players</h1>
          <p className="text-zinc-400 text-sm mt-1">{allPlayers.length} players in this set</p>
        </div>
        <Link href="/checklists" className="text-sm text-zinc-400 hover:text-white transition-colors">
          &larr; Back to set
        </Link>
      </div>

      <div className="rounded-xl border border-zinc-800 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-zinc-800 bg-zinc-900">
              <th className="text-left px-4 py-3 text-zinc-400 font-medium">Player</th>
              <th className="text-right px-4 py-3 text-zinc-400 font-medium">Cards</th>
              <th className="text-right px-4 py-3 text-zinc-400 font-medium hidden sm:table-cell">
                Numbered
              </th>
              <th className="text-right px-4 py-3 text-zinc-400 font-medium hidden md:table-cell">
                Insert Sets
              </th>
              <th className="text-right px-4 py-3 text-zinc-400 font-medium hidden md:table-cell">
                1/1s
              </th>
            </tr>
          </thead>
          <tbody>
            {allPlayers.map((player, i) => (
              <tr
                key={player.id}
                className={`border-b border-zinc-800/60 hover:bg-zinc-900/50 transition-colors ${
                  i === allPlayers.length - 1 ? "border-b-0" : ""
                }`}
              >
                <td className="px-4 py-3">
                  <Link
                    href={`/players/${player.id}`}
                    className="text-zinc-100 hover:text-white font-medium hover:underline"
                  >
                    {player.name}
                  </Link>
                </td>
                <td className="px-4 py-3 text-right text-zinc-300 font-mono">
                  {player.uniqueCards}
                </td>
                <td className="px-4 py-3 text-right text-zinc-400 font-mono hidden sm:table-cell">
                  {player.totalPrintRun > 0 ? player.totalPrintRun : "—"}
                </td>
                <td className="px-4 py-3 text-right text-zinc-400 hidden md:table-cell">
                  {player.insertSetCount}
                </td>
                <td className="px-4 py-3 text-right hidden md:table-cell">
                  {player.oneOfOnes > 0 ? (
                    <span className="text-amber-400 font-semibold">Yes</span>
                  ) : (
                    <span className="text-zinc-600">—</span>
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
