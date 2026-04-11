function RankBadge({ rank }: { rank: number }) {
  const colors =
    rank === 1
      ? "bg-amber-500/20 text-amber-400 border-amber-500/40"
      : rank === 2
        ? "bg-zinc-400/15 text-zinc-300 border-zinc-400/30"
        : rank === 3
          ? "bg-orange-500/15 text-orange-400 border-orange-500/30"
          : "bg-zinc-800 text-zinc-500 border-zinc-700";
  return (
    <span
      className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold border ${colors}`}
    >
      {rank}
    </span>
  );
}

function PrintRunBadge({ printRun }: { printRun: string }) {
  const isUltraRare = printRun === "/1" || printRun === "/5";
  const isRare = printRun === "/10" || printRun === "/25";
  const color = isUltraRare
    ? "text-red-400"
    : isRare
      ? "text-amber-400"
      : "text-zinc-400";
  return <span className={`text-sm font-semibold ${color}`}>{printRun}</span>;
}

export function ChaseTable({
  cards,
}: {
  cards: Array<{
    rank: number;
    cardName: string;
    athlete: string;
    printRun: string;
    boxType: string;
    odds: string;
  }>;
}) {
  return (
    <div className="rounded-xl border border-zinc-800 overflow-hidden mb-6">
      <table className="w-full">
        <thead>
          <tr className="border-b border-zinc-800 bg-zinc-900/60">
            <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-2.5 w-10">
              #
            </th>
            <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-2.5">
              Card
            </th>
            <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-2.5 hidden sm:table-cell">
              Print Run
            </th>
            <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-2.5 hidden md:table-cell">
              Box Type
            </th>
            <th className="text-right text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-2.5">
              Odds
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-800/60">
          {cards.map((card) => (
            <tr
              key={card.rank}
              className="bg-zinc-900 hover:bg-zinc-800/40 transition-colors"
            >
              <td className="px-4 py-3">
                <RankBadge rank={card.rank} />
              </td>
              <td className="px-4 py-3">
                <p className="text-[15px] font-semibold text-zinc-200">
                  {card.cardName}
                </p>
                <p className="text-[13px] text-zinc-500">{card.athlete}</p>
              </td>
              <td className="px-4 py-3 hidden sm:table-cell">
                <PrintRunBadge printRun={card.printRun} />
              </td>
              <td className="px-4 py-3 hidden md:table-cell">
                <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-400 border border-zinc-700">
                  {card.boxType}
                </span>
              </td>
              <td className="px-4 py-3 text-right">
                <span className="text-[13px] text-zinc-500 tabular-nums">
                  {card.odds}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
