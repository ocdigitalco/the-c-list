// Checklist² Brand System — shared primitives
// Locked from v1 · 01 (two-card mark, Inter Tight wordmark)

const CL2 = {
  ink: '#0E0E0E',
  paper: '#F1EDE4',
  accent: '#D63A20',
  inkSoft: '#2A241C',
  paperDeep: '#E5E0D3',
  accentDeep: '#B12C18',
  accentSoft: '#F2A192',
  slate: '#5A5247',
  fog: '#CFC8B8',
  fontHead: '"Inter Tight", "Inter", system-ui, sans-serif',
  fontBody: '"Inter", system-ui, sans-serif',
  fontMono: '"JetBrains Mono", ui-monospace, Menlo, monospace'
};

const CARD_RATIO_W = 2.5;
const CARD_RATIO_H = 3.5;

// Two-card mark — canonical
function CL2Mark({ s = 120, front = CL2.ink, back = CL2.accent, bg = 'transparent' }) {
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
    <svg width={s} height={s} viewBox={`0 0 ${s} ${s}`} shapeRendering="crispEdges" style={{ display: 'block', background: bg, overflow: 'visible' }}>
      <rect x={bx} y={by} width={cardW} height={cardH} fill={back} />
      <rect x={fx} y={fy} width={cardW} height={cardH} fill={front} />
    </svg>);

}

// Wordmark
function CL2Wordmark({ size = 96, ink = CL2.ink, accent = CL2.accent }) {
  return (
    <div style={{
      fontFamily: CL2.fontHead, fontWeight: 800, fontSize: size, color: ink,
      letterSpacing: -size * 0.042, lineHeight: 0.9,
      display: 'inline-flex', alignItems: 'flex-start'
    }}>
      <span>Checklist</span>
      <span style={{
        fontSize: size * 0.54, color: accent, fontWeight: 900,
        marginTop: -size * 0.083, marginLeft: size * 0.02, letterSpacing: 0, padding: "0px"
      }}>2</span>
    </div>);

}

// Lockup
function CL2Lockup({ size = 96, ink = CL2.ink, accent = CL2.accent, bg = 'transparent' }) {
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: size * 0.19 }}>
      <CL2Mark s={size * 1.17} front={ink} back={accent} bg={bg} />
      <CL2Wordmark size={size} ink={ink} accent={accent} />
    </div>);

}

// C² Avatar — favicon / social / app icon
// theme: 'dark' (ink tile, paper C, accent ²) — DEFAULT
//        'light' (paper tile, ink C, accent ²)
//        'red' (accent tile, paper C, ink ²)
//        'card' (two-card geometry, ink front w/ paper C, accent back)
function CL2AppIcon({ s = 256, theme = 'dark', radius = 0 }) {
  if (theme === 'card') {
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
      <svg width={s} height={s} viewBox={`0 0 ${s} ${s}`} style={{ display: 'block', overflow: 'visible', borderRadius: radius }}>
        <rect x={bx} y={by} width={cardW} height={cardH} fill={CL2.accent} />
        <rect x={fx} y={fy} width={cardW} height={cardH} fill={CL2.ink} />
        <text x={cX} y={cY} fontFamily={CL2.fontHead} fontWeight="900" fontSize={fontPx} fill={CL2.paper} textAnchor="middle" dominantBaseline="central" letterSpacing={-fontPx * 0.04}>C</text>
        <text x={fx + cardW * 0.84} y={fy + cardH * 0.24} fontFamily={CL2.fontHead} fontWeight="900" fontSize={supPx} fill={CL2.accent} textAnchor="middle" dominantBaseline="central">2</text>
      </svg>);

  }
  let tileBg, letter, sup;
  if (theme === 'dark') {tileBg = CL2.ink;letter = CL2.paper;sup = CL2.accent;}
  if (theme === 'light') {tileBg = CL2.paper;letter = CL2.ink;sup = CL2.accent;}
  if (theme === 'red') {tileBg = CL2.accent;letter = CL2.paper;sup = CL2.ink;}
  const fontPx = s * 0.74;
  const supPx = fontPx * 0.42;
  return (
    <svg width={s} height={s} viewBox={`0 0 ${s} ${s}`} style={{ display: 'block', borderRadius: radius }}>
      <rect x={0} y={0} width={s} height={s} fill={tileBg} />
      <text x={s * 0.46} y={s * 0.55} fontFamily={CL2.fontHead} fontWeight="900" fontSize={fontPx} fill={letter} textAnchor="middle" dominantBaseline="central" letterSpacing={-fontPx * 0.04}>C</text>
      <text x={s * 0.80} y={s * 0.30} fontFamily={CL2.fontHead} fontWeight="900" fontSize={supPx} fill={sup} textAnchor="middle" dominantBaseline="central">2</text>
    </svg>);

}

Object.assign(window, { CL2, CL2Mark, CL2Wordmark, CL2Lockup, CL2AppIcon });