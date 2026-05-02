/**
 * Checklist² Brand System
 *
 * Ported 1:1 from brand-system.jsx. All numeric ratios are intentional
 * and must be preserved exactly.
 */

// ─── Tokens ─────────────────────────────────────────────────────────────────────

export const CL2 = {
  ink: "#0E0E0E",
  paper: "#F1EDE4",
  accent: "#D63A20",
  inkSoft: "#2A241C",
  paperDeep: "#E5E0D3",
  accentDeep: "#B12C18",
  accentSoft: "#F2A192",
  slate: "#5A5247",
  fog: "#CFC8B8",
  fontHead: '"Inter Tight", "Inter", system-ui, sans-serif',
  fontBody: '"Inter", system-ui, sans-serif',
  fontMono: '"JetBrains Mono", ui-monospace, Menlo, monospace',
} as const;

const CARD_RATIO_W = 2.5;
const CARD_RATIO_H = 3.5;

// ─── CL2Mark ────────────────────────────────────────────────────────────────────

interface MarkProps {
  s?: number;
  front?: string;
  back?: string;
  bg?: string;
}

export function CL2Mark({
  s = 120,
  front = CL2.ink,
  back = CL2.accent,
  bg = "transparent",
}: MarkProps) {
  const cardH = s * 0.78;
  const cardW = cardH * (CARD_RATIO_W / CARD_RATIO_H);
  const offsetY = 0.18;
  const offsetX = 1.4 * offsetY;
  const totalW = cardW * (1 + offsetX);
  const totalH = cardH * (1 + offsetY);
  const fx = (s - totalW) / 2;
  const fy = (s - totalH) / 2 + cardH * offsetY;
  const bx = fx + cardW * offsetX;
  const by = fy - cardH * offsetY;

  return (
    <svg
      width={s}
      height={s}
      viewBox={`0 0 ${s} ${s}`}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ display: "block" }}
      shapeRendering="crispEdges"
    >
      {bg !== "transparent" && (
        <rect width={s} height={s} fill={bg} />
      )}
      <rect x={bx} y={by} width={cardW} height={cardH} fill={back} />
      <rect x={fx} y={fy} width={cardW} height={cardH} fill={front} />
    </svg>
  );
}

// ─── CL2Wordmark ────────────────────────────────────────────────────────────────

interface WordmarkProps {
  size?: number;
  supSize?: number;
  ink?: string;
  accent?: string;
}

export function CL2Wordmark({
  size = 96,
  supSize,
  ink = CL2.ink,
  accent = CL2.accent,
}: WordmarkProps) {
  const supFontSize = supSize ?? size * 0.54;
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "flex-start",
        fontFamily: CL2.fontHead,
        lineHeight: 0.9,
      }}
    >
      <span
        style={{
          fontSize: size,
          fontWeight: 800,
          letterSpacing: -size * 0.042,
          color: ink,
        }}
      >
        Checklist
      </span>
      <span
        style={{
          fontSize: supFontSize,
          fontWeight: 900,
          color: accent,
          marginTop: -size * 0.083,
          marginLeft: size * 0.02,
        }}
      >
        &#178;
      </span>
    </span>
  );
}

// ─── CL2Lockup ──────────────────────────────────────────────────────────────────

interface LockupProps {
  size?: number;
  ink?: string;
  accent?: string;
  bg?: string;
}

export function CL2Lockup({
  size = 96,
  ink = CL2.ink,
  accent = CL2.accent,
  bg = "transparent",
}: LockupProps) {
  const gap = size * 0.19;
  const markSize = size * 1.17;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap,
        background: bg,
      }}
    >
      <CL2Mark s={markSize} front={ink} back={accent} />
      <CL2Wordmark size={size} ink={ink} accent={accent} />
    </span>
  );
}

// ─── CL2AppIcon ─────────────────────────────────────────────────────────────────

type AppIconTheme = "dark" | "light" | "red" | "card";

interface AppIconProps {
  s?: number;
  theme?: AppIconTheme;
  radius?: number;
}

export function CL2AppIcon({
  s = 256,
  theme = "dark",
  radius = 0,
}: AppIconProps) {
  const themes: Record<string, { tileBg: string; letter: string; sup: string }> = {
    dark: { tileBg: CL2.ink, letter: CL2.paper, sup: CL2.accent },
    light: { tileBg: CL2.paper, letter: CL2.ink, sup: CL2.accent },
    red: { tileBg: CL2.accent, letter: CL2.paper, sup: CL2.ink },
  };

  if (theme === "card") {
    const cardH = s * 0.86;
    const cardW = cardH * (CARD_RATIO_W / CARD_RATIO_H);
    const offsetY = 0.10;
    const offsetX = 1.4 * offsetY;
    const totalW = cardW * (1 + offsetX);
    const totalH = cardH * (1 + offsetY);
    const fx = (s - totalW) / 2;
    const fy = (s - totalH) / 2 + cardH * offsetY;
    const bx = fx + cardW * offsetX;
    const by = fy - cardH * offsetY;
    const fontPx = cardH * 0.78;
    const cX = fx + cardW * 0.46;
    const cY = fy + cardH * 0.54;
    const supPx = fontPx * 0.42;

    return (
      <svg width={s} height={s} viewBox={`0 0 ${s} ${s}`} xmlns="http://www.w3.org/2000/svg"
        style={{ display: "block" }} shapeRendering="crispEdges">
        <rect width={s} height={s} fill={CL2.ink} rx={radius} />
        <rect x={bx} y={by} width={cardW} height={cardH} fill={CL2.accent} />
        <rect x={fx} y={fy} width={cardW} height={cardH} fill={CL2.ink} />
        <text x={cX} y={cY} fill={CL2.paper}
          fontFamily="Inter Tight" fontWeight={900} fontSize={fontPx}
          textAnchor="middle" dominantBaseline="central"
          letterSpacing={-fontPx * 0.04}>C</text>
        <text x={fx + cardW * 0.84} y={fy + cardH * 0.24} fill={CL2.accent}
          fontFamily="Inter Tight" fontWeight={900} fontSize={supPx}
          textAnchor="middle" dominantBaseline="central">&#178;</text>
      </svg>
    );
  }

  const t = themes[theme] ?? themes.dark;
  const fontPx = s * 0.74;
  const supPx = fontPx * 0.42;

  return (
    <svg width={s} height={s} viewBox={`0 0 ${s} ${s}`} xmlns="http://www.w3.org/2000/svg"
      style={{ display: "block" }}>
      <rect width={s} height={s} fill={t.tileBg} rx={radius} />
      <text x={s * 0.46} y={s * 0.55} fill={t.letter}
        fontFamily="Inter Tight" fontWeight={900} fontSize={fontPx}
        textAnchor="middle" dominantBaseline="central"
        letterSpacing={-fontPx * 0.04}>C</text>
      <text x={s * 0.80} y={s * 0.30} fill={t.sup}
        fontFamily="Inter Tight" fontWeight={900} fontSize={supPx}
        textAnchor="middle" dominantBaseline="central">&#178;</text>
    </svg>
  );
}
