const VARIANTS = {
  tip: {
    border: "border-l-amber-500",
    bg: "bg-amber-950/20",
    label: "text-amber-400",
    text: "text-amber-200/80",
  },
  warning: {
    border: "border-l-red-500",
    bg: "bg-red-950/20",
    label: "text-red-400",
    text: "text-red-200/80",
  },
  exclusive: {
    border: "border-l-blue-500",
    bg: "bg-blue-950/20",
    label: "text-blue-400",
    text: "text-blue-200/80",
  },
  info: {
    border: "border-l-zinc-500",
    bg: "bg-zinc-800/40",
    label: "text-zinc-400",
    text: "text-zinc-300",
  },
} as const;

export function CalloutBlock({
  variant,
  label,
  text,
}: {
  variant: keyof typeof VARIANTS;
  label: string;
  text: string;
}) {
  const v = VARIANTS[variant];
  return (
    <div
      className={`my-6 border-l-[3px] ${v.border} ${v.bg} rounded-r-lg px-5 py-4`}
    >
      <p
        className={`text-[11px] font-bold uppercase tracking-widest ${v.label} mb-1.5`}
      >
        {label}
      </p>
      <p className={`text-[15px] leading-relaxed ${v.text}`}>{text}</p>
    </div>
  );
}
