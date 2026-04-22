// Procedural SVG card-art placeholder — striped / gradient abstract art per sport.
// NOT drawing people. Deterministic from set id so each set has a consistent look.

function hashStr(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return Math.abs(h);
}

function CardArt({ set, width = 240, height = 336 }) {
  const palette = window.SPORT_PALETTES[set.sport] || window.SPORT_PALETTES.other;
  const [c1, c2, c3] = palette;
  const h = hashStr(set.id);
  const variant = h % 5;
  const angle = (h % 60) - 30;
  const tier = (set.tiers && set.tiers[0]) || '';
  const gid = `g-${set.id}`;
  const lid = `l-${set.id}`;
  const mid = `m-${set.id}`;

  const tierMark = tier ? tier.toUpperCase() : (set.leagues[0] || '').toUpperCase();

  return (
    <svg viewBox={`0 0 ${width} ${height}`} width="100%" height="100%" preserveAspectRatio="xMidYMid slice" style={{display:'block'}}>
      <defs>
        <linearGradient id={gid} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor={c1} />
          <stop offset="1" stopColor={c2} />
        </linearGradient>
        <linearGradient id={lid} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="rgba(255,255,255,0.18)" />
          <stop offset="0.5" stopColor="rgba(255,255,255,0)" />
          <stop offset="1" stopColor="rgba(0,0,0,0.35)" />
        </linearGradient>
        <pattern id={mid} width="8" height="8" patternUnits="userSpaceOnUse" patternTransform={`rotate(${angle})`}>
          <rect width="8" height="8" fill="transparent" />
          <rect width="1" height="8" fill="rgba(255,255,255,0.12)" />
        </pattern>
      </defs>

      <rect width={width} height={height} fill={`url(#${gid})`} />

      {/* Variant-specific abstract composition */}
      {variant === 0 && (
        <>
          <circle cx={width*0.5} cy={height*0.55} r={height*0.42} fill={c3} opacity="0.28" />
          <circle cx={width*0.5} cy={height*0.55} r={height*0.3}  fill={c1} opacity="0.35" />
          <rect x="0" y={height*0.55} width={width} height={2} fill={c3} opacity="0.5" />
        </>
      )}
      {variant === 1 && (
        <>
          <polygon points={`0,${height} ${width*0.6},0 ${width},0 ${width},${height*0.4} ${width*0.4},${height}`} fill={c3} opacity="0.28" />
          <polygon points={`0,${height*0.25} ${width*0.55},${height} 0,${height}`} fill={c2} opacity="0.35" />
        </>
      )}
      {variant === 2 && (
        <>
          {[...Array(7)].map((_,i)=>(
            <rect key={i} x={-20} y={i*(height/7)} width={width+40} height={height/14} fill={i%2?c3:c1} opacity={0.22} transform={`rotate(-8 ${width/2} ${height/2})`}/>
          ))}
        </>
      )}
      {variant === 3 && (
        <>
          <circle cx={width*0.2} cy={height*0.25} r={height*0.28} fill={c3} opacity="0.35" />
          <circle cx={width*0.8} cy={height*0.8} r={height*0.35} fill={c2} opacity="0.4" />
          <rect x={width*0.15} y={height*0.15} width={width*0.7} height={height*0.7} fill="none" stroke={c3} strokeWidth="2" opacity="0.5" />
        </>
      )}
      {variant === 4 && (
        <>
          <rect x={width*0.1} y={height*0.1} width={width*0.8} height={height*0.8} fill={c3} opacity="0.18" />
          <rect x={width*0.18} y={height*0.18} width={width*0.64} height={height*0.64} fill="none" stroke={c3} strokeWidth="1" opacity="0.6" />
          <line x1="0" y1={height*0.65} x2={width} y2={height*0.65} stroke={c3} strokeWidth="1" opacity="0.45" />
        </>
      )}

      {/* Universal overlays: stripes + gloss + tier mark */}
      <rect width={width} height={height} fill={`url(#${mid})`} />
      <rect width={width} height={height} fill={`url(#${lid})`} />

      {/* Subtle corner tier badge */}
      {tierMark && (
        <g>
          <text x={12} y={22} fontFamily="ui-monospace, 'JetBrains Mono', Menlo, monospace" fontSize="9" fontWeight="700" fill={c3} opacity="0.9" letterSpacing="2">
            {tierMark.slice(0,10)}
          </text>
          <text x={width-12} y={height-12} textAnchor="end" fontFamily="ui-monospace, 'JetBrains Mono', Menlo, monospace" fontSize="9" fontWeight="700" fill={c3} opacity="0.75" letterSpacing="2">
            {String(set.year)}
          </text>
        </g>
      )}

      {/* Frame */}
      <rect x="0.5" y="0.5" width={width-1} height={height-1} fill="none" stroke="rgba(0,0,0,0.25)" />
    </svg>
  );
}

window.CardArt = CardArt;
