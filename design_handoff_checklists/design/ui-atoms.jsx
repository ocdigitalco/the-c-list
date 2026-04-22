// Shared small UI atoms

function Chip({ children, tone = 'default' }) {
  const tones = {
    default: { background: '#F1EFE9', color: '#3A372F', border: '1px solid #E6E3D9' },
    dark:    { background: '#151412', color: '#F6F3EA', border: '1px solid #151412' },
    accent:  { background: 'oklch(0.55 0.17 25)', color: '#FFF8F1', border: '1px solid oklch(0.5 0.17 25)' },
  };
  const s = tones[tone] || tones.default;
  return (
    <span style={{
      display:'inline-flex', alignItems:'center', padding:'3px 9px',
      fontSize:11, fontWeight:500, letterSpacing:0.2,
      borderRadius: 4,
      ...s,
    }}>{children}</span>
  );
}

function IconSearch({ size = 16, color = '#8A8677' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <circle cx="11" cy="11" r="7" stroke={color} strokeWidth="1.6"/>
      <path d="M20 20L16.5 16.5" stroke={color} strokeWidth="1.6" strokeLinecap="round"/>
    </svg>
  );
}

function IconGrid({ size = 14, color = '#1A1916' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <rect x="3" y="3" width="8" height="8" rx="1" fill={color}/>
      <rect x="13" y="3" width="8" height="8" rx="1" fill={color}/>
      <rect x="3" y="13" width="8" height="8" rx="1" fill={color}/>
      <rect x="13" y="13" width="8" height="8" rx="1" fill={color}/>
    </svg>
  );
}

function IconRows({ size = 14, color = '#1A1916' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <rect x="3" y="4" width="18" height="4" rx="1" fill={color}/>
      <rect x="3" y="10" width="18" height="4" rx="1" fill={color}/>
      <rect x="3" y="16" width="18" height="4" rx="1" fill={color}/>
    </svg>
  );
}

function IconChev({ dir = 'left', size = 14, color = '#3A372F' }) {
  const rot = { left: 180, right: 0, up: 270, down: 90 }[dir] || 0;
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" style={{transform:`rotate(${rot}deg)`}}>
      <path d="M9 6l6 6-6 6" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconX({ size = 14, color = '#3A372F' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path d="M6 6l12 12M18 6L6 18" stroke={color} strokeWidth="1.8" strokeLinecap="round"/>
    </svg>
  );
}

function IconSliders({ size = 14, color = '#1A1916' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path d="M4 7h10M18 7h2M4 12h2M10 12h10M4 17h14M20 17h0" stroke={color} strokeWidth="1.6" strokeLinecap="round"/>
      <circle cx="16" cy="7" r="2" fill={color}/>
      <circle cx="8" cy="12" r="2" fill={color}/>
      <circle cx="18" cy="17" r="2" fill={color}/>
    </svg>
  );
}

Object.assign(window, { Chip, IconSearch, IconGrid, IconRows, IconChev, IconX, IconSliders });
