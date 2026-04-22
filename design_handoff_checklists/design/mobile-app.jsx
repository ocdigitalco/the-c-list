// Mobile Checklists — iOS adaptation

function MobileApp() {
  const [sport, setSport] = React.useState('all');
  const [query, setQuery] = React.useState('');
  const [openId, setOpenId] = React.useState(null);
  const [view, setView] = React.useState('gallery'); // 'gallery' or 'compact'

  const sets = window.SETS;
  const filtered = React.useMemo(() => {
    const q = query.trim().toLowerCase();
    return sets.filter(s => {
      if (sport !== 'all' && s.sport !== sport) return false;
      if (!q) return true;
      const hay = [s.name, s.sport, ...(s.leagues||[]), ...(s.tiers||[]), String(s.year)].join(' ').toLowerCase();
      return hay.includes(q);
    });
  }, [sport, query, sets]);

  const openSet = openId ? sets.find(s => s.id === openId) : null;

  return (
    <IOSDevice width={402} height={874}>
      {openSet ? (
        <MobileDetail set={openSet} onBack={()=>setOpenId(null)}/>
      ) : (
        <MobileIndex
          sets={filtered} allSets={sets}
          sport={sport} setSport={setSport}
          query={query} setQuery={setQuery}
          view={view} setView={setView}
          onOpen={setOpenId}
        />
      )}
    </IOSDevice>
  );
}

function MobileIndex({ sets, allSets, sport, setSport, query, setQuery, view, setView, onOpen }) {
  const featured = allSets.filter(s => s.featured).slice(0, 5);
  return (
    <div style={{
      paddingTop: 54,
      paddingBottom: 40,
      background:'#FAFAF7',
      minHeight:'100%',
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
          fontSize:34, fontWeight:700, letterSpacing:-0.9,
          margin:'12px 0 4px', color:'#0F0F0E', lineHeight:1,
        }}>Checklists</h1>
        <p style={{color:'#6B6757', fontSize:14, margin:0}}>
          Browse all sports card sets
        </p>
      </div>

      {/* Search */}
      <div style={{padding:'18px 20px 0'}}>
        <div style={{
          background:'#F1EFE9', borderRadius:12,
          display:'flex', alignItems:'center', padding:'0 14px',
          height:40,
        }}>
          <IconSearch/>
          <input
            value={query}
            onChange={e=>setQuery(e.target.value)}
            placeholder="Search sets, leagues, tiers..."
            style={{
              flex:1, border:'none', background:'transparent', outline:'none',
              padding:'0 10px', fontSize:15, color:'#0F0F0E',
              fontFamily:'inherit',
            }}
          />
          {query && (
            <button onClick={()=>setQuery('')} style={{
              background:'none', border:'none', cursor:'pointer', padding:2,
              display:'flex', alignItems:'center',
            }}>
              <IconX size={14} color="#6B6757"/>
            </button>
          )}
        </div>
      </div>

      {/* Sport filter — horizontal scroll chips */}
      <div style={{
        display:'flex', gap:6, overflowX:'auto', padding:'14px 20px 6px',
        scrollbarWidth:'none',
      }} className="no-scrollbar">
        {window.SPORTS.map(s => {
          const active = s.id === sport;
          return (
            <button key={s.id} onClick={()=>setSport(s.id)} style={{
              flex:'0 0 auto',
              padding: active ? '7px 14px' : '7px 12px',
              borderRadius:999,
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

      {/* Featured strip removed — using ribbons on cards instead */}

      {/* Results header + view toggle */}
      <div style={{
        display:'flex', alignItems:'center', justifyContent:'space-between',
        padding:'22px 20px 12px',
      }}>
        <div style={{display:'flex', alignItems:'baseline', gap:8}}>
          <span style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:10, letterSpacing:1.5, color:'#0F0F0E', fontWeight:600,
          }}>
            {sport==='all' ? 'ALL SETS' : window.SPORTS.find(s=>s.id===sport).label.toUpperCase()}
          </span>
          <span style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:10, letterSpacing:1.5, color:'#B7B2A3', fontWeight:500,
          }}>{sets.length}</span>
        </div>
        <div style={{display:'flex', gap:2, background:'#F1EFE9', borderRadius:8, padding:3}}>
          <button onClick={()=>setView('gallery')} style={{
            width:28, height:28, borderRadius:6, border:'none',
            background: view==='gallery' ? '#0F0F0E' : 'transparent',
            display:'flex', alignItems:'center', justifyContent:'center', cursor:'pointer',
          }}>
            <IconGrid size={12} color={view==='gallery' ? '#FAFAF7' : '#1A1916'}/>
          </button>
          <button onClick={()=>setView('compact')} style={{
            width:28, height:28, borderRadius:6, border:'none',
            background: view==='compact' ? '#0F0F0E' : 'transparent',
            display:'flex', alignItems:'center', justifyContent:'center', cursor:'pointer',
          }}>
            <IconRows size={12} color={view==='compact' ? '#FAFAF7' : '#1A1916'}/>
          </button>
        </div>
      </div>

      {/* Grid / List */}
      {sets.length === 0 ? (
        <div style={{
          margin:'30px 20px', padding:'40px 20px',
          border:'1px dashed #D9D5C7', borderRadius:12, textAlign:'center',
          color:'#8A8677', fontSize:13,
        }}>No sets match your filters.</div>
      ) : view==='gallery' ? (
        <div style={{
          display:'grid', gridTemplateColumns:'1fr 1fr',
          gap:14, rowGap:22, padding:'0 20px',
        }}>
          {sets.map(s => (
            <div key={s.id} onClick={()=>onOpen(s.id)} style={{cursor:'pointer'}}>
              <div style={{
                aspectRatio:'2/2.8', overflow:'hidden',
                background:'#EAE6D9', position:'relative',
                boxShadow:'0 1px 2px rgba(15,15,14,0.08)',
              }}>
                <CardArt set={s} width={180} height={252}/>
                {s.featured && (
                  <div style={{
                    position:'absolute', top:8, left:-3,
                    background:'oklch(0.55 0.17 25)', color:'#FFF8F1',
                    fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                    fontSize:8, letterSpacing:1.2, fontWeight:700,
                    padding:'3px 6px 3px 8px',
                    clipPath:'polygon(0 0, 100% 0, 100% 100%, 0 100%, 3px 50%)',
                    boxShadow:'0 2px 4px rgba(0,0,0,0.15)',
                  }}>RECENTLY ADDED</div>
                )}
              </div>
              <div style={{marginTop:8}}>
                <div style={{
                  fontFamily:'"Inter Tight", Inter, sans-serif',
                  fontSize:13, fontWeight:600, color:'#0F0F0E', letterSpacing:-0.2,
                  lineHeight:1.25,
                }}>{s.name}</div>
                <div style={{
                  marginTop:5,
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:10, color:'#6B6757',
                }}>
                  {s.athletes} athletes · {s.cards.toLocaleString()} cards
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{padding:'0 16px', display:'flex', flexDirection:'column', gap:8}}>
          {sets.map(s => (
            <div key={s.id} onClick={()=>onOpen(s.id)} style={{
              display:'flex', alignItems:'center', gap:12,
              padding:'10px', background:'#FFFFFF',
              border:'1px solid #EDEAE0', borderRadius:10,
              cursor:'pointer',
            }}>
              <div style={{width:52, height:72, overflow:'hidden', flex:'0 0 auto', background:'#EAE6D9', position:'relative'}}>
                <CardArt set={s} width={52} height={72}/>
                {s.featured && (
                  <div style={{
                    position:'absolute', top:4, left:-2,
                    background:'oklch(0.55 0.17 25)', color:'#FFF8F1',
                    fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                    fontSize:7, letterSpacing:0.8, fontWeight:700,
                    padding:'2px 4px 2px 5px',
                    clipPath:'polygon(0 0, 100% 0, 100% 100%, 0 100%, 2px 50%)',
                  }}>NEW</div>
                )}
              </div>
              <div style={{flex:1, minWidth:0}}>
                <div style={{
                  fontFamily:'"Inter Tight", Inter, sans-serif',
                  fontSize:14, fontWeight:600, color:'#0F0F0E', letterSpacing:-0.2,
                  lineHeight:1.25,
                }}>{s.name}</div>
                <div style={{display:'flex', gap:5, marginTop:5, flexWrap:'wrap'}}>
                  {s.leagues.slice(0,1).map(l=>(<Chip key={l}>{l}</Chip>))}
                  {s.tiers.slice(0,1).map(t=>(<Chip key={t} tone="dark">{t}</Chip>))}
                </div>
                <div style={{
                  marginTop:6,
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:10, color:'#6B6757',
                }}>
                  {s.athletes} athletes · {s.cards.toLocaleString()} cards
                </div>
              </div>
              <IconChev dir="right" size={12} color="#B7B2A3"/>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function MobileDetail({ set, onBack }) {
  const [tab, setTab] = React.useState('Base');
  const tabs = ['Base', 'Inserts', 'Parallels', 'Autographs'];
  const names = ['K. Owens', 'M. Reyes', 'T. Abara', 'J. Sato', 'L. Kovacs', 'R. Bakr', 'D. Njoku', 'A. Volkov',
    'C. Park', 'S. Marquez', 'B. Haruna', 'N. Okafor', 'P. Weiss', 'E. Tomori'];
  const cards = names.map((n, i) => ({
    num: String(i+1).padStart(3,'0'),
    name: n,
    team: ['North','South','East','West'][i%4] + ' ' + ['Apex','Vanguard','Heritage','Legion'][i%4],
    variant: i%7===0 ? 'SP' : (i%5===0 ? 'RC' : ''),
  }));

  return (
    <div style={{
      paddingTop:54, paddingBottom:40,
      background:'#FAFAF7', minHeight:'100%',
      fontFamily:'-apple-system, system-ui, sans-serif',
    }}>
      <div style={{padding:'8px 20px 0'}}>
        <button onClick={onBack} style={{
          display:'inline-flex', alignItems:'center', gap:4,
          background:'none', border:'none', padding:'6px 0', cursor:'pointer',
          color:'#6B6757', fontSize:15, fontFamily:'inherit',
        }}>
          <svg width="8" height="14" viewBox="0 0 8 14"><path d="M7 1L1 7l6 6" stroke="#6B6757" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" fill="none"/></svg>
          Checklists
        </button>
      </div>

      <div style={{padding:'16px 20px 0', display:'flex', gap:16}}>
        <div style={{
          width:120, height:168,
          overflow:'hidden', background:'#EAE6D9',
          boxShadow:'0 12px 28px rgba(15,15,14,0.18)',
          flex:'0 0 auto',
        }}>
          <CardArt set={set} width={120} height={168}/>
        </div>
        <div style={{flex:1, minWidth:0}}>
          <div style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:9, letterSpacing:1.5, color:'#8A8677', fontWeight:500,
          }}>{(set.leagues[0]||'').toUpperCase()} · {set.year}</div>
          <h2 style={{
            fontFamily:'"Inter Tight", Inter, sans-serif',
            fontSize:20, fontWeight:700, letterSpacing:-0.5,
            margin:'6px 0 0', color:'#0F0F0E', lineHeight:1.15,
          }}>{set.name}</h2>
          <div style={{display:'flex', gap:5, marginTop:10, flexWrap:'wrap'}}>
            {set.leagues.map(l=>(<Chip key={l}>{l}</Chip>))}
            {set.tiers.map(t=>(<Chip key={t} tone="dark">{t}</Chip>))}
          </div>
        </div>
      </div>

      <div style={{
        display:'grid', gridTemplateColumns:'1fr 1fr', gap:1,
        margin:'18px 20px 0', background:'#EDEAE0', overflow:'hidden', borderRadius:10,
      }}>
        <MStat label="ATHLETES" value={set.athletes}/>
        <MStat label="CARDS" value={set.cards.toLocaleString()}/>
      </div>

      <div style={{padding:'16px 20px 0', display:'flex', flexDirection:'column', gap:8}}>
        <button style={{
          width:'100%', padding:'13px', background:'#0F0F0E', color:'#FAFAF7',
          border:'none', borderRadius:10, fontFamily:'inherit', fontSize:14, fontWeight:600, cursor:'pointer',
        }}>Track my collection</button>
      </div>

      <div style={{
        display:'flex', gap:2, margin:'22px 20px 0',
        borderBottom:'1px solid #EDEAE0',
      }}>
        {tabs.map(t => (
          <button key={t} onClick={()=>setTab(t)} style={{
            padding:'10px 12px', background:'none', border:'none',
            borderBottom: tab===t ? '2px solid #0F0F0E' : '2px solid transparent',
            marginBottom:-1,
            color: tab===t ? '#0F0F0E' : '#8A8677',
            fontFamily:'inherit', fontSize:13,
            fontWeight: tab===t ? 600 : 400, cursor:'pointer',
          }}>{t}</button>
        ))}
      </div>

      <div style={{padding:'4px 20px 0'}}>
        {cards.map((c, i) => (
          <div key={c.num} style={{
            display:'flex', alignItems:'center', gap:12,
            padding:'12px 4px', borderBottom:'1px solid #F4F1E8',
          }}>
            <div style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              color:'#8A8677', fontSize:11, width:32,
            }}>{c.num}</div>
            <div style={{flex:1, minWidth:0}}>
              <div style={{fontSize:14, fontWeight:500, color:'#0F0F0E'}}>{c.name}</div>
              <div style={{fontSize:11, color:'#6B6757', marginTop:1}}>{c.team}</div>
            </div>
            {c.variant && <Chip tone={c.variant==='SP'?'accent':'default'}>{c.variant}</Chip>}
            <input type="checkbox" defaultChecked={i%4===0}
              style={{width:18, height:18, accentColor:'#0F0F0E', cursor:'pointer'}}/>
          </div>
        ))}
      </div>
    </div>
  );
}

function MStat({ label, value }) {
  return (
    <div style={{background:'#FAFAF7', padding:'12px 14px'}}>
      <div style={{
        fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize:9, letterSpacing:1.5, color:'#B7B2A3', fontWeight:500,
      }}>{label}</div>
      <div style={{
        fontFamily:'"Inter Tight", Inter, sans-serif',
        fontSize:18, fontWeight:700, color:'#0F0F0E',
        letterSpacing:-0.4, marginTop:2,
      }}>{value}</div>
    </div>
  );
}

const mobileRoot = ReactDOM.createRoot(document.getElementById('root'));
mobileRoot.render(
  <div style={{
    minHeight:'100vh', background:'#E8E5DB',
    display:'flex', alignItems:'center', justifyContent:'center',
    padding:'40px 20px',
  }}>
    <MobileApp/>
  </div>
);
