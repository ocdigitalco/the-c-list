// Sets Coverage — mobile (iOS frame)

const M_GREEN = '#0E8A4F';
const M_GRAY = '#B7B2A3';
const M_RED = '#C2410C';

function mFmtDate(iso) {
  if (!iso) return null;
  const d = new Date(iso + 'T00:00:00');
  const m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getMonth()];
  return `${m} ${d.getDate()}`;
}

function setIsComplete(s) {
  return s.checklist && s.parallels && s.boxConfig && s.packOdds && !!s.releaseDate;
}

function setMissingCount(s) {
  let n = 0;
  if (!s.checklist) n++;
  if (!s.parallels) n++;
  if (!s.boxConfig) n++;
  if (!s.packOdds) n++;
  if (!s.releaseDate) n++;
  return n;
}

function MMfrPill({ mfr }) {
  const isPanini = mfr === 'panini';
  const label = isPanini ? 'Panini' : 'Topps';
  return (
    <span style={{
      display:'inline-flex', alignItems:'center', justifyContent:'center',
      padding:'2px 7px',
      fontSize:10, fontWeight:600, letterSpacing:0.2,
      borderRadius:3,
      background: isPanini ? '#F2C230' : 'transparent',
      color: isPanini ? '#1A1916' : '#E11D48',
      border: isPanini ? '1px solid #E0B41E' : '1px solid #E11D48',
      fontFamily:'inherit',
    }}>{label}</span>
  );
}

// Compact 5-dot strip (one dot per coverage field)
function CoverageDots({ set }) {
  const fields = [
    { ok: set.checklist,        k: 'C', tip: 'Checklist' },
    { ok: !!set.releaseDate,    k: 'D', tip: 'Release Date' },
    { ok: set.parallels,        k: 'P', tip: 'Parallels' },
    { ok: set.boxConfig,        k: 'B', tip: 'Box Config' },
    { ok: set.packOdds,         k: 'O', tip: 'Pack Odds' },
  ];
  return (
    <div style={{display:'inline-flex', gap:3, alignItems:'center'}}>
      {fields.map((f, i) => (
        <span key={i} title={f.tip} style={{
          display:'inline-flex', alignItems:'center', justifyContent:'center',
          width:16, height:16, borderRadius:4,
          background: f.ok ? 'rgba(14,138,79,0.12)' : 'rgba(183,178,163,0.18)',
          color: f.ok ? M_GREEN : M_GRAY,
          fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize:8, fontWeight:700, letterSpacing:0,
        }}>{f.k}</span>
      ))}
    </div>
  );
}

function mOpenChecklist(set) {
  try {
    if (set.checklistId || set.id) {
      localStorage.setItem('cl_openId', set.checklistId || set.id);
    }
  } catch (e) {}
  window.location.href = 'Checklists Mobile.html';
}

function MSetRow({ set }) {
  const complete = setIsComplete(set);
  const missing = setMissingCount(set);
  return (
    <a
      href="Checklists Mobile.html"
      onClick={(e) => { e.preventDefault(); mOpenChecklist(set); }}
      style={{
        display:'block',
        padding:'12px 14px',
        background:'#FFFFFF',
        borderTop:'1px solid #F1EEE3',
        textDecoration:'none', color:'inherit', cursor:'pointer',
      }}>
      <div style={{display:'flex', alignItems:'center', gap:8, marginBottom:6}}>
        <MMfrPill mfr={set.mfr}/>
        <span style={{
          fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize:9, color:'#8A8677', letterSpacing:0.6,
        }}>{set.releaseDate ? mFmtDate(set.releaseDate) : 'NO DATE'}</span>
        <span style={{flex:1}}/>
        {complete ? (
          <span style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:9, color:M_GREEN, fontWeight:600, letterSpacing:0.6,
          }}>READY</span>
        ) : (
          <span style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:9, color:M_RED, fontWeight:600, letterSpacing:0.6,
          }}>{missing} MISSING</span>
        )}
      </div>
      <div style={{
        fontFamily:'"Inter Tight", -apple-system, Inter, sans-serif',
        fontSize:14, fontWeight:600, color:'#0F0F0E', letterSpacing:-0.2,
        lineHeight:1.25, marginBottom:8,
      }}>{set.name}</div>
      <CoverageDots set={set}/>
    </a>
  );
}

function MSportGroup({ sport, sets }) {
  const label = window.COVERAGE_SPORTS.find(s => s.id === sport)?.label || sport;
  return (
    <div style={{marginTop:18}}>
      <div style={{
        fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize:9, letterSpacing:1.6, color:'#3A372F', fontWeight:600,
        padding:'0 14px 8px',
      }}>{label.toUpperCase()}</div>
      <div style={{
        margin:'0 14px',
        background:'#FFFFFF',
        border:'1px solid #EDEAE0',
        borderRadius:10,
        overflow:'hidden',
      }}>
        {sets.map(s => <MSetRow key={s.id} set={s}/>)}
      </div>
    </div>
  );
}

function MYearSection({ year, sets, defaultOpen }) {
  const [open, setOpen] = React.useState(defaultOpen);
  const complete = sets.filter(setIsComplete).length;

  const bySport = {};
  for (const s of sets) (bySport[s.sport] ||= []).push(s);
  const sportOrder = window.COVERAGE_SPORTS
    .map(x => x.id).filter(id => id !== 'all' && bySport[id]);

  return (
    <div style={{marginTop:24}}>
      <button onClick={()=>setOpen(o=>!o)} style={{
        width:'100%', display:'flex', alignItems:'center', gap:10,
        padding:'10px 14px', background:'none', border:'none', cursor:'pointer',
        textAlign:'left', fontFamily:'inherit',
        borderBottom:'1px solid #EDEAE0',
      }}>
        <svg width="11" height="11" viewBox="0 0 12 12" style={{
          transform: open ? 'rotate(0deg)' : 'rotate(-90deg)',
          transition:'transform 0.15s ease',
        }}>
          <path d="M2 4l4 4 4-4" stroke="#3A372F" strokeWidth="1.6" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <span style={{
          fontFamily:'"Inter Tight", -apple-system, Inter, sans-serif',
          fontSize:18, fontWeight:700, letterSpacing:-0.4, color:'#0F0F0E',
        }}>{year}</span>
        <span style={{flex:1}}/>
        <span style={{
          fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize:10, color:'#8A8677',
        }}>{complete}/{sets.length}</span>
      </button>

      {open && sportOrder.map(sp => (
        <MSportGroup key={sp} sport={sp} sets={bySport[sp]}/>
      ))}
    </div>
  );
}

function MobileCoverageApp() {
  const [mfr, setMfr] = React.useState('all');
  const [sport, setSport] = React.useState('all');
  const [onlyIncomplete, setOnlyIncomplete] = React.useState(false);
  const [legendOpen, setLegendOpen] = React.useState(false);

  const sets = window.COVERAGE_SETS;
  const filtered = React.useMemo(() => sets.filter(s => {
    if (mfr !== 'all' && s.mfr !== mfr) return false;
    if (sport !== 'all' && s.sport !== sport) return false;
    if (onlyIncomplete && setIsComplete(s)) return false;
    return true;
  }), [mfr, sport, onlyIncomplete, sets]);

  const totalTracked = sets.length;
  const totalAll = 840;

  const byYear = {};
  for (const s of filtered) (byYear[s.year] ||= []).push(s);
  const years = Object.keys(byYear).map(Number).sort((a,b)=>b-a);

  return (
    <IOSDevice width={402} height={874}>
      <div style={{
        paddingTop:54, paddingBottom:40,
        background:'#FAFAF7', minHeight:'100%',
        fontFamily:'-apple-system, system-ui, sans-serif',
        color:'#0F0F0E',
      }}>
        {/* Header */}
        <div style={{padding:'10px 20px 0'}}>
          <button style={{
            display:'inline-flex', alignItems:'center', gap:4,
            background:'none', border:'none', padding:0, cursor:'pointer',
            color:'#6B6757', fontSize:15, fontFamily:'inherit',
          }}>
            <svg width="8" height="14" viewBox="0 0 8 14"><path d="M7 1L1 7l6 6" stroke="#6B6757" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" fill="none"/></svg>
            Home
          </button>
          <h1 style={{
            fontFamily:'"Inter Tight", -apple-system, Inter, sans-serif',
            fontSize:30, fontWeight:700, letterSpacing:-0.8,
            margin:'12px 0 4px', color:'#0F0F0E', lineHeight:1,
          }}>Sets Coverage</h1>
          <p style={{color:'#6B6757', fontSize:13, margin:0}}>
            <span style={{color:'#0F0F0E', fontWeight:600}}>{totalTracked}</span>
            {' '}of <span style={{color:'#0F0F0E', fontWeight:600}}>{totalAll}</span> sets tracked
          </p>
        </div>

        {/* Legend (collapsible) */}
        <div style={{padding:'14px 20px 0'}}>
          <button onClick={()=>setLegendOpen(o=>!o)} style={{
            width:'100%', textAlign:'left',
            background:'#FFFFFF', border:'1px solid #EDEAE0',
            borderRadius:10, padding:'10px 12px',
            display:'flex', alignItems:'center', gap:8, cursor:'pointer',
            fontFamily:'inherit',
          }}>
            <CoverageDots set={{checklist:true,releaseDate:'2026-01-01',parallels:true,boxConfig:true,packOdds:true}}/>
            <span style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:10, letterSpacing:1.4, color:'#3A372F', fontWeight:600,
            }}>REQUIRED COVERAGE</span>
            <span style={{flex:1}}/>
            <svg width="10" height="10" viewBox="0 0 12 12" style={{
              transform: legendOpen ? 'rotate(180deg)' : 'rotate(0deg)',
              transition:'transform 0.15s ease',
            }}>
              <path d="M2 4l4 4 4-4" stroke="#3A372F" strokeWidth="1.6" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
          {legendOpen && (
            <div style={{
              marginTop:6, padding:'10px 12px',
              background:'#FFFFFF', border:'1px solid #EDEAE0', borderRadius:10,
              display:'grid', gridTemplateColumns:'1fr 1fr', rowGap:8, columnGap:10,
            }}>
              {[
                {k:'C', label:'Checklist'},
                {k:'D', label:'Release Date'},
                {k:'P', label:'Parallels'},
                {k:'B', label:'Box Config'},
                {k:'O', label:'Pack Odds'},
              ].map(f => (
                <span key={f.k} style={{
                  display:'inline-flex', alignItems:'center', gap:6,
                  fontSize:12, color:'#3A372F',
                }}>
                  <span style={{
                    display:'inline-flex', alignItems:'center', justifyContent:'center',
                    width:16, height:16, borderRadius:4,
                    background:'rgba(14,138,79,0.12)', color:M_GREEN,
                    fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                    fontSize:8, fontWeight:700,
                  }}>{f.k}</span>
                  {f.label}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Manufacturer chips */}
        <div style={{
          display:'flex', gap:6, overflowX:'auto', padding:'14px 20px 0',
          scrollbarWidth:'none',
        }} className="no-scrollbar">
          <span style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:9, letterSpacing:1.4, color:'#8A8677',
            alignSelf:'center', marginRight:2, flex:'0 0 auto',
          }}>MFR</span>
          {window.MANUFACTURERS.map(o => {
            const active = o.id === mfr;
            const isAll = o.id === 'all';
            const isPan = o.id === 'panini';
            const isTpps = o.id === 'topps';
            let bg='#FFFFFF', color='#3A372F', border='1px solid #E6E3D9';
            if (active) {
              if (isAll) { bg='#0F0F0E'; color='#FAFAF7'; border='1px solid #0F0F0E'; }
              else if (isPan) { bg='#F2C230'; color='#1A1916'; border='1px solid #E0B41E'; }
              else if (isTpps) { bg='#FFFFFF'; color='#E11D48'; border='1px solid #E11D48'; }
            } else {
              if (isPan) color = '#B47A0F';
              if (isTpps) color = '#E11D48';
            }
            return (
              <button key={o.id} onClick={()=>setMfr(o.id)} style={{
                flex:'0 0 auto',
                padding:'7px 12px', borderRadius:999, background:bg, color, border,
                fontFamily:'inherit', fontSize:13,
                fontWeight: active ? 600 : 500,
                cursor:'pointer', whiteSpace:'nowrap',
              }}>{o.label}</button>
            );
          })}
        </div>

        {/* Sport chips */}
        <div style={{
          display:'flex', gap:6, overflowX:'auto', padding:'8px 20px 0',
          scrollbarWidth:'none',
        }} className="no-scrollbar">
          <span style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:9, letterSpacing:1.4, color:'#8A8677',
            alignSelf:'center', marginRight:2, flex:'0 0 auto',
          }}>SPORT</span>
          {window.COVERAGE_SPORTS.map(s => {
            const active = s.id === sport;
            return (
              <button key={s.id} onClick={()=>setSport(s.id)} style={{
                flex:'0 0 auto',
                padding:'7px 12px', borderRadius:999,
                border: active ? '1px solid #0F0F0E' : '1px solid #E6E3D9',
                background: active ? '#0F0F0E' : '#FFFFFF',
                color: active ? '#FAFAF7' : '#3A372F',
                fontFamily:'inherit', fontSize:13,
                fontWeight: active ? 600 : 500,
                cursor:'pointer', whiteSpace:'nowrap',
              }}>{s.label}</button>
            );
          })}
        </div>

        {/* Incomplete toggle */}
        <div style={{padding:'12px 20px 0'}}>
          <button onClick={()=>setOnlyIncomplete(v=>!v)} style={{
            display:'inline-flex', alignItems:'center', gap:8,
            padding:'7px 12px', borderRadius:999,
            background: onlyIncomplete ? '#0F0F0E' : '#FFFFFF',
            color: onlyIncomplete ? '#FAFAF7' : '#3A372F',
            border: onlyIncomplete ? '1px solid #0F0F0E' : '1px solid #E6E3D9',
            fontFamily:'inherit', fontSize:12, fontWeight:500, cursor:'pointer',
          }}>
            <span style={{
              width:14, height:14, borderRadius:3,
              border: onlyIncomplete ? '1px solid #FAFAF7' : '1px solid #B7B2A3',
              background: onlyIncomplete ? '#FAFAF7' : 'transparent',
              display:'inline-flex', alignItems:'center', justifyContent:'center',
              color:'#0F0F0E', fontSize:10, fontWeight:700,
            }}>{onlyIncomplete ? '✓' : ''}</span>
            Show only incomplete
          </button>
        </div>

        {/* Year sections */}
        {years.length === 0 ? (
          <div style={{
            margin:'30px 20px', padding:'40px 20px',
            border:'1px dashed #D9D5C7', borderRadius:12, textAlign:'center',
            color:'#8A8677', fontSize:13,
          }}>No sets match these filters.</div>
        ) : years.map((y, i) => (
          <MYearSection key={y} year={y} sets={byYear[y]} defaultOpen={i === 0}/>
        ))}
      </div>
    </IOSDevice>
  );
}

const mCovRoot = ReactDOM.createRoot(document.getElementById('root'));
mCovRoot.render(
  <div style={{
    minHeight:'100vh', background:'#E8E5DB',
    display:'flex', alignItems:'center', justifyContent:'center',
    padding:'40px 20px',
  }}>
    <MobileCoverageApp/>
  </div>
);
