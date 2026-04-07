interface Props {
  label: string;
  value: number | string;
  subtext?: string;
}

export function V2StatCard({ label, value, subtext }: Props) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 border-t-4 border-t-indigo-500">
      <p className="text-[11px] font-semibold text-zinc-500 uppercase tracking-wider mb-1">{label}</p>
      <p className="text-2xl sm:text-3xl font-bold text-indigo-400 tabular-nums">
        {typeof value === "number" ? value.toLocaleString() : value}
      </p>
      {subtext && <p className="text-[11px] text-zinc-600 mt-1">{subtext}</p>}
    </div>
  );
}
