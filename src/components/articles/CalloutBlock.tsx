const VARIANTS = {
  tip: {
    border: "border-l-amber-500",
    bg: "bg-amber-950/20",
    labelColor: "#444441",
    textColor: "#1A1A1A",
  },
  warning: {
    border: "border-l-red-500",
    bg: "bg-red-950/20",
    labelColor: "rgba(255,255,255,0.75)",
    textColor: "#FFFFFF",
  },
  exclusive: {
    border: "border-l-blue-500",
    bg: "bg-blue-950/20",
    labelColor: "rgba(255,255,255,0.75)",
    textColor: "#FFFFFF",
  },
  info: {
    border: "border-l-zinc-500",
    bg: "bg-zinc-800/40",
    labelColor: "#444441",
    textColor: "#1A1A1A",
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
        className="text-[11px] font-bold uppercase tracking-widest mb-1.5"
        style={{ color: v.labelColor }}
      >
        {label}
      </p>
      <p
        className="text-[15px] leading-relaxed"
        style={{ color: v.textColor }}
      >
        {text}
      </p>
    </div>
  );
}
