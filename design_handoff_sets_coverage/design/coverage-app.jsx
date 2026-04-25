// Sets Coverage admin page — uses Checklists.html visual system.

const ACCENT_GREEN = '#0E8A4F';
const MISSING_GRAY = '#B7B2A3';

function fmtDate(iso) {
  if (!iso) return null;
  const d = new Date(iso + 'T00:00:00');
  const m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getMonth()];
  return `${m} ${d.getDate()}, ${d.getFullYear()}`;
}

function MfrPill({ mfr }) {
  const m = window.MANUFACTURERS.find(x => x.id === mfr);
  if (!m) return null;
  const isPanini = m.id === 'panini';
  return (
    <span style={{
      display:'inline-flex', alignItems:'center', justifyContent:'center',
      minWidth: 56, padding:'4px 10px',
      fontFamily:'inherit', fontSize:11, fontWeight:600,
      letterSpacing: 0.2,
      borderRadius: 4,
      background: isPanini ? '#F2C230' : 'transparent',
      color: isPanini ? '#1A1916' : '#E11D48',
      border: isPanini ? '1px solid #E0B41E' : '1px solid #E11D48',
    }}>{m.label}</span>
  );
}

function CoverageMark({ ok, label, dateLabel }) {
  const color = ok ? ACCENT_GREEN : MISSING_GRAY;
  const icon = ok ? '✓' : '✗';
  return (
    <span style={{
      display:'inline-flex', alignItems:'center', gap:5,
      color, fontSize:13, fontFamily:'inherit',
      whiteSpace:'nowrap',
    }}>
      <span style={{fontSize:13, fontWeight:600, lineHeight:1}}>{icon}</span>
      <span>{dateLabel ?? label}</span>
    </span>
  );
}

function openChecklist(set) {
  try {
    if (set.checklistId || set.id) {
      localStorage.setItem('cl_openId', set.checklistId || set.id);
    }
  } catch (e) {}
  window.location.href = 'Checklists.html';
}

function SetRow({ set, isLast }) {
  return (
    <a
      href="Checklists.html"
      onClick={(e) => { e.preventDefault(); openChecklist(set); }}
      style={{
        display:'grid',
        gridTemplateColumns: '92px 1fr auto',
        alignItems:'center',
        gap:18,
        padding:'14px 18px',
        background:'#FFFFFF',
        borderTop: '1px solid #F1EEE3',
        textDecoration:'none', color:'inherit', cursor:'pointer',
      }}
      onMouseEnter={e => e.currentTarget.style.background = '#FDFCF8'}
      onMouseLeave={e => e.currentTarget.style.background = '#FFFFFF'}
    >
      <MfrPill mfr={set.mfr}/>
      <div style={{
        fontFamily:'"Inter Tight", Inter, sans-serif',
        fontSize:14, fontWeight:500, color:'#0F0F0E',
        letterSpacing:-0.1, minWidth:0,
        overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap',
      }}>{set.name}</div>
      <div style={{display:'flex', gap:22, alignItems:'center'}}>
        <CoverageMark ok={set.checklist} label="Checklist"/>
        <CoverageMark ok={!!set.releaseDate} label="Release Date"
          dateLabel={set.releaseDate ? fmtDate(set.releaseDate) : 'No date'}/>
        <CoverageMark ok={set.parallels} label="Parallels"/>
        <CoverageMark ok={set.boxConfig} label="Box Config"/>
        <CoverageMark ok={set.packOdds} label="Pack Odds"/>
      </div>
    </a>
  );
}

function SportGroup({ sport, sets }) {
  const label = window.COVERAGE_SPORTS.find(s => s.id === sport)?.label || sport;
  return (
    <div style={{marginTop:22}}>
      <div style={{
        fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize:10, letterSpacing:2, color:'#3A372F', fontWeight:600,
        padding:'0 4px 10px',
      }}>{label.toUpperCase()}</div>
      <div style={{
        background:'#FFFFFF',
        border:'1px solid #EDEAE0',
        borderRadius: 10,
        overflow:'hidden',
      }}>
        {sets.map((s, i) => (
          <SetRow key={s.id} set={s} isLast={i === sets.length - 1}/>
        ))}
      </div>
    </div>
  );
}

function YearSection({ year, sets, defaultOpen }) {
  const [open, setOpen] = React.useState(defaultOpen);
  const complete = sets.filter(s =>
    s.checklist && s.parallels && s.boxConfig && s.packOdds && !!s.releaseDate
  ).length;

  // Group by sport, preserving sport order
  const bySport = {};
  for (const s of sets) (bySport[s.sport] ||= []).push(s);
  const sportOrder = window.COVERAGE_SPORTS.map(x => x.id).filter(id => id !== 'all' && bySport[id]);

  return (
    <div style={{marginTop:32}}>
      <button onClick={()=>setOpen(o=>!o)} style={{
        width:'100%', display:'flex', alignItems:'center', gap:12,
        padding:'10px 0', background:'none', border:'none', cursor:'pointer',
        textAlign:'left', fontFamily:'inherit',
        borderBottom:'1px solid #EDEAE0',
      }}>
        <span style={{
          display:'inline-flex', alignItems:'center', justifyContent:'center',
          width:22, height:22, color:'#3A372F',
        }}>
          <svg width="12" height="12" viewBox="0 0 12 12" style={{
            transform: open ? 'rotate(0deg)' : 'rotate(-90deg)',
            transition: 'transform 0.15s ease',
          }}>
            <path d="M2 4l4 4 4-4" stroke="#3A372F" strokeWidth="1.6" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </span>
        <span style={{
          fontFamily:'"Inter Tight", Inter, sans-serif',
          fontSize:22, fontWeight:600, letterSpacing:-0.5, color:'#0F0F0E',
        }}>{year}</span>
        <span style={{flex:1}}/>
        <span style={{
          fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize:11, color:'#8A8677',
        }}>{complete} / {sets.length} complete</span>
      </button>

      {open && (
        <div>
          {sportOrder.map(sp => (
            <SportGroup key={sp} sport={sp} sets={bySport[sp]}/>
          ))}
        </div>
      )}
    </div>
  );
}

function FilterRow({ label, options, active, onChange, mfrPills }) {
  return (
    <div style={{display:'flex', alignItems:'center', gap:16, marginTop:18}}>
      <div style={{
        fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize:10, letterSpacing:2, color:'#8A8677', fontWeight:500,
        width: 110,
      }}>{label}</div>
      <div style={{display:'flex', gap:6, flexWrap:'wrap', flex:1}}>
        {options.map(o => {
          const isActive = o.id === active;
          if (mfrPills) {
            const isAll = o.id === 'all';
            const isPan = o.id === 'panini';
            const isTpps = o.id === 'topps';
            let bg = 'transparent', color = '#3A372F', border = '1px solid transparent';
            if (isActive) {
              if (isAll) { bg = '#0F0F0E'; color = '#FAFAF7'; border = '1px solid #0F0F0E'; }
              else if (isPan) { bg = '#F2C230'; color = '#1A1916'; border = '1px solid #E0B41E'; }
              else if (isTpps) { bg = 'transparent'; color = '#E11D48'; border = '1px solid #E11D48'; }
            } else {
              if (isPan) color = '#B47A0F';
              if (isTpps) color = '#E11D48';
            }
            return (
              <button key={o.id} onClick={()=>onChange(o.id)} style={{
                padding:'6px 14px', borderRadius: 999,
                background: bg, color, border,
                fontFamily:'inherit', fontSize:13,
                fontWeight: isActive ? 600 : 500,
                cursor:'pointer', transition:'all 0.15s ease',
              }}>{o.label}</button>
            );
          }
          return (
            <button key={o.id} onClick={()=>onChange(o.id)}
              style={{
                padding: isActive ? '6px 14px' : '6px 12px',
                borderRadius: 999,
                border: isActive ? '1px solid #0F0F0E' : '1px solid transparent',
                background: isActive ? '#0F0F0E' : 'transparent',
                color: isActive ? '#FAFAF7' : '#3A372F',
                fontFamily:'inherit', fontSize:13,
                fontWeight: isActive ? 500 : 400,
                cursor:'pointer', transition:'all 0.15s ease',
                whiteSpace:'nowrap',
              }}
              onMouseEnter={e=>{ if(!isActive) e.currentTarget.style.background='#F1EFE9'; }}
              onMouseLeave={e=>{ if(!isActive) e.currentTarget.style.background='transparent'; }}
            >{o.label}</button>
          );
        })}
      </div>
    </div>
  );
}

function CoveragePage() {
  const [mfr, setMfr] = React.useState('all');
  const [sport, setSport] = React.useState('all');
  const [onlyIncomplete, setOnlyIncomplete] = React.useState(false);

  const sets = window.COVERAGE_SETS;
  const filtered = React.useMemo(() => {
    return sets.filter(s => {
      if (mfr !== 'all' && s.mfr !== mfr) return false;
      if (sport !== 'all' && s.sport !== sport) return false;
      if (onlyIncomplete) {
        const ok = s.checklist && s.parallels && s.boxConfig && s.packOdds && !!s.releaseDate;
        if (ok) return false;
      }
      return true;
    });
  }, [mfr, sport, onlyIncomplete, sets]);

  const totalTracked = sets.length;
  const totalAll = 840; // app-wide stat

  // Group by year, descending
  const byYear = {};
  for (const s of filtered) (byYear[s.year] ||= []).push(s);
  const years = Object.keys(byYear).map(Number).sort((a,b)=>b-a);

  return (
    <div style={{
      minHeight:'100vh', background:'#FAFAF7',
      fontFamily:'Inter, system-ui, -apple-system, sans-serif', color:'#0F0F0E',
    }}>
      <div style={{maxWidth:1440, margin:'0 auto', padding:'40px 56px 80px'}}>
        <button style={{
          display:'inline-flex', alignItems:'center', gap:6,
          background:'none', border:'none', padding:0, cursor:'pointer',
          color:'#6B6757', fontSize:13, fontFamily:'inherit',
        }}>
          <svg width="8" height="14" viewBox="0 0 8 14"><path d="M7 1L1 7l6 6" stroke="#6B6757" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" fill="none"/></svg>
          Home
        </button>
        <h1 style={{
          fontFamily:'"Inter Tight", Inter, system-ui, sans-serif',
          fontSize: 48, fontWeight: 600, letterSpacing: -1.2,
          margin:'14px 0 8px', color:'#0F0F0E', lineHeight:1,
        }}>Sets Coverage</h1>
        <p style={{ color:'#6B6757', fontSize:14, margin:0 }}>
          <span style={{color:'#0F0F0E', fontWeight:600}}>{totalTracked.toLocaleString()}</span>
          {' '}of <span style={{color:'#0F0F0E', fontWeight:600}}>{totalAll.toLocaleString()}</span> sets tracked in the app
        </p>

        {/* Coverage legend strip */}
        <div style={{
          marginTop:24, padding:'14px 18px',
          background:'#FFFFFF', border:'1px solid #EDEAE0', borderRadius:10,
          display:'flex', alignItems:'center', gap:24, flexWrap:'wrap',
        }}>
          <div style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:10, letterSpacing:2, color:'#3A372F', fontWeight:600,
          }}>REQUIRED COVERAGE</div>
          {window.COVERAGE_FIELDS.map(f => (
            <span key={f.key} style={{
              display:'inline-flex', alignItems:'center', gap:6,
              fontSize:13, color:'#3A372F',
            }}>
              <span style={{
                width:6, height:6, borderRadius:999, background:ACCENT_GREEN,
              }}/>
              {f.label}
            </span>
          ))}
          <span style={{flex:1}}/>
          <button onClick={()=>setOnlyIncomplete(v=>!v)} style={{
            padding:'6px 12px', borderRadius:999,
            background: onlyIncomplete ? '#0F0F0E' : 'transparent',
            color: onlyIncomplete ? '#FAFAF7' : '#3A372F',
            border: onlyIncomplete ? '1px solid #0F0F0E' : '1px solid #D9D5C7',
            fontFamily:'inherit', fontSize:12, fontWeight:500,
            cursor:'pointer',
          }}>{onlyIncomplete ? '✓ ' : ''}Show only incomplete</button>
        </div>

        <div style={{marginTop:14}}>
          <FilterRow label="MANUFACTURER" options={window.MANUFACTURERS}
            active={mfr} onChange={setMfr} mfrPills/>
          <FilterRow label="SPORT" options={window.COVERAGE_SPORTS}
            active={sport} onChange={setSport}/>
        </div>

        {years.length === 0 ? (
          <div style={{
            marginTop:40, padding:'80px 20px', textAlign:'center',
            border:'1px dashed #D9D5C7', borderRadius:12, color:'#8A8677',
          }}>
            <div style={{fontSize:14, marginBottom:6, color:'#3A372F', fontWeight:500}}>No sets match these filters.</div>
            <div style={{fontSize:12}}>Try clearing filters or toggling "Show only incomplete".</div>
          </div>
        ) : (
          years.map((y, i) => (
            <YearSection key={y} year={y} sets={byYear[y]} defaultOpen={i === 0}/>
          ))
        )}
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<CoveragePage/>);
