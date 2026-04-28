// Option D — Mobile
// Same content as desktop D, restructured for narrow viewport:
//   - Sticky compact header with hamburger that opens the Athletes drawer
//   - Drawer is 100% width × 100% height when open (per spec)
//   - Hero card → meta → 6 stat tiles (3 cols) → primary tabs → tab content
//   - Pack Odds tab uses a horizontal scrollable chip row for box-types

function OptionDMobile() {
  const s = window.SET_DETAIL;
  const [tab, setTab] = React.useState('Box Config');
  const [boxTab, setBoxTab] = React.useState('Hobby');
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [athleteFilter, setAthleteFilter] = React.useState('Total Cards');
  const tabs = ['Box Config', 'Pack Odds', 'Inserts', 'Autographs'];
  const athleteFilters = ['Total Cards', 'Autographs', 'Inserts', 'Numbered'];

  const boxExclusives = {
    Hobby:  ['Exclusive Red, White, and Blue Refractors'],
    Jumbo:  ['Exclusive Hot Pink and Lime Green X-Fractors'],
    Mega:   ['Exclusive Pulsar Refractors'],
  };

  return (
    <div style={{
      width:'100%', minHeight:'100%', background:'#FAFAF7',
      color:'#0F0F0E', fontFamily:'Inter, system-ui, sans-serif',
      paddingTop:54, // status-bar safe space
      position:'relative',
    }}>
      {/* APP TOP BAR — sticky */}
      <div style={{
        position:'sticky', top:54, zIndex:10,
        background:'rgba(250,250,247,0.92)', backdropFilter:'blur(12px)',
        WebkitBackdropFilter:'blur(12px)',
        borderBottom:'1px solid #EDEAE0',
        padding:'12px 16px', display:'flex', alignItems:'center', gap:10,
      }}>
        <button onClick={()=>setDrawerOpen(true)} aria-label="Athletes" style={{
          background:'#FFFFFF', border:'1px solid #E6E3D9', borderRadius:8,
          padding:'8px 10px', display:'flex', alignItems:'center', gap:6,
          fontSize:12, fontWeight:500, color:'#3A372F', cursor:'pointer',
          fontFamily:'inherit',
        }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <circle cx="9" cy="8" r="3.2" stroke="#3A372F" strokeWidth="1.6"/>
            <circle cx="17" cy="9" r="2.4" stroke="#3A372F" strokeWidth="1.6"/>
            <path d="M3.5 18c.6-2.6 2.7-4.2 5.5-4.2s4.9 1.6 5.5 4.2" stroke="#3A372F" strokeWidth="1.6" strokeLinecap="round"/>
            <path d="M15 16c.4-1.4 1.5-2.4 3-2.4 1.5 0 2.6 1 3 2.4" stroke="#3A372F" strokeWidth="1.6" strokeLinecap="round"/>
          </svg>
          Athletes <span style={{color:'#8A8677'}}>· {s.athletes}</span>
        </button>
        <span style={{flex:1}}/>
        <button style={{
          background:'#0F0F0E', color:'#FAFAF7', border:'none', borderRadius:8,
          padding:'8px 12px', fontSize:12, fontWeight:600, cursor:'pointer',
          fontFamily:'inherit',
        }}>↓ Break Sheet</button>
      </div>

      {/* HERO */}
      <div style={{padding:'18px 16px 14px', background:'#FFFFFF', borderBottom:'1px solid #EDEAE0'}}>
        <div style={{display:'flex', gap:14, alignItems:'flex-start'}}>
          <div style={{
            aspectRatio:'2/2.8', background:'linear-gradient(150deg, #C2102E 0%, #6B0A1B 100%)',
            position:'relative', overflow:'hidden', height:108, width:78,
            boxShadow:'0 8px 18px rgba(15,15,14,0.18)',
            transform:'rotate(-3deg)', flex:'0 0 auto',
          }}>
            <div style={{position:'absolute', top:7, left:7, right:7,
              fontSize:7, fontWeight:700, color:'#FFF', letterSpacing:1.2,
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            }}>PATRIOTS</div>
            <div style={{position:'absolute', bottom:8, left:8, color:'#FFF'}}>
              <div style={{fontSize:9, fontWeight:700, fontFamily:'"Inter Tight", sans-serif'}}>DRAKE MAYE</div>
              <div style={{fontSize:7, opacity:0.85, marginTop:1, letterSpacing:1}}>QB · /5</div>
            </div>
          </div>
          <div style={{flex:1, minWidth:0}}>
            <div style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:9, letterSpacing:1.6, color:'#8A8677', fontWeight:600,
            }}>NFL · CHROME · {s.released.toUpperCase()}</div>
            <h1 style={{
              fontFamily:'"Inter Tight", Inter, sans-serif',
              fontSize:24, fontWeight:600, letterSpacing:-0.6,
              margin:'4px 0 8px', lineHeight:1.05, color:'#0F0F0E',
            }}>{s.name}</h1>
            <div style={{display:'flex', gap:5, alignItems:'center', flexWrap:'wrap'}}>
              <Chip>NFL</Chip>
              <Chip tone="dark">Chrome</Chip>
              <span style={{fontSize:11, color:'#6B6757', marginLeft:2}}>547 athletes</span>
            </div>
          </div>
        </div>
      </div>

      {/* STAT GRID — 3×2 */}
      <div style={{
        display:'grid', gridTemplateColumns:'repeat(3, 1fr)',
        background:'#FFFFFF', borderBottom:'1px solid #EDEAE0',
      }}>
        {[
          ['CARDS', s.cards.toLocaleString()],
          ['CARD TYPES', s.cardTypes],
          ['PARALLEL TYPES', s.parallelTypes],
          ['AUTOS', s.autographs],
          ['AUTO PARALLELS', s.autoParallels.toLocaleString()],
          ['TOTAL PARALLELS', s.totalParallels.toLocaleString()],
        ].map(([label, val], i) => {
          const col = i % 3;
          const row = Math.floor(i / 3);
          return (
            <div key={label} style={{
              padding:'14px 12px',
              borderRight: col < 2 ? '1px solid #EDEAE0' : 'none',
              borderBottom: row === 0 ? '1px solid #EDEAE0' : 'none',
            }}>
              <div style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:8, letterSpacing:1.4, color:'#8A8677', fontWeight:600,
              }}>{label}</div>
              <div style={{
                fontFamily:'"Inter Tight", Inter, sans-serif',
                fontSize:20, fontWeight:600, letterSpacing:-0.5, color:'#0F0F0E',
                marginTop:3,
              }}>{val}</div>
            </div>
          );
        })}
      </div>

      {/* TABS — sticky, horizontal scroll */}
      <div style={{
        position:'sticky', top: 54 + 41, zIndex:9,
        display:'flex', gap:0, padding:'0 16px',
        background:'#FAFAF7', borderBottom:'1px solid #EDEAE0',
        overflowX:'auto', WebkitOverflowScrolling:'touch',
      }}>
        {tabs.map(t => (
          <button key={t} onClick={()=>setTab(t)} style={{
            padding:'12px 14px', background:'none', border:'none',
            borderBottom: tab===t ? '2px solid #0F0F0E' : '2px solid transparent',
            marginBottom:-1, color: tab===t ? '#0F0F0E' : '#8A8677',
            fontFamily:'inherit', fontSize:13, whiteSpace:'nowrap',
            fontWeight: tab===t ? 600 : 500, cursor:'pointer',
          }}>{t}</button>
        ))}
      </div>

      {/* CONTENT */}
      <main style={{padding:'16px'}}>
        {tab === 'Box Config' && (
          <div>
            {window.BOX_CONFIG.map(r => {
              const ex = boxExclusives[r.type];
              return (
                <div key={r.type} style={{
                  background:'#FFFFFF', border:'1px solid #EDEAE0', borderRadius:10,
                  padding:'12px 14px', marginBottom:10,
                }}>
                  <div style={{
                    fontFamily:'"Inter Tight", sans-serif', fontSize:15, fontWeight:600,
                    marginBottom:8,
                  }}>{r.type}</div>
                  <div style={{
                    display:'grid', gridTemplateColumns:'repeat(5, 1fr)', gap:6,
                  }}>
                    {[
                      ['CARDS/PACK', r.cardsPerPack],
                      ['PACKS/BOX', r.packsPerBox],
                      ['BOXES/CASE', r.boxesPerCase],
                      ['PACKS/CASE', r.packsPerCase],
                      ['AUTOS/BOX', r.autosPerBox],
                    ].map(([k, v]) => (
                      <div key={k}>
                        <div style={{
                          fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                          fontSize:7, letterSpacing:1.2, color:'#8A8677', fontWeight:600,
                        }}>{k}</div>
                        <div style={{
                          fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                          fontSize:14, fontWeight:600,
                          color: v == null ? '#B7B2A3' : '#0F0F0E',
                          marginTop:2,
                        }}>{v ?? '—'}</div>
                      </div>
                    ))}
                  </div>
                  {ex && (
                    <div style={{
                      marginTop:10, paddingTop:10, borderTop:'1px solid #F4F1E8',
                    }}>
                      {ex.map(n => (
                        <div key={n} style={{
                          fontStyle:'italic', fontSize:11, color:'#6B6757',
                        }}>{n}</div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {tab === 'Pack Odds' && (
          <div>
            <div style={{
              display:'flex', gap:6, marginBottom:14,
              overflowX:'auto', WebkitOverflowScrolling:'touch',
              paddingBottom:4,
            }}>
              {window.PACK_ODDS_TABS.map(t => {
                const active = t === boxTab;
                return (
                  <button key={t} onClick={()=>setBoxTab(t)} style={{
                    padding:'7px 12px', borderRadius:999, fontSize:12,
                    fontFamily:'inherit', fontWeight: active ? 600 : 500,
                    background: active ? '#0F0F0E' : '#FFFFFF',
                    color: active ? '#FAFAF7' : '#3A372F',
                    border: active ? '1px solid #0F0F0E' : '1px solid #EDEAE0',
                    cursor:'pointer', whiteSpace:'nowrap',
                  }}>{t}</button>
                );
              })}
            </div>
            <div style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:8, letterSpacing:1.4, color:'#8A8677', fontWeight:600,
              padding:'4px 4px 8px', borderBottom:'1px solid #EDEAE0',
              marginBottom:4,
            }}>BASE PARALLELS</div>
            {window.BASE_PARALLELS.map(p => (
              <div key={p.name} style={{
                padding:'10px 4px', borderBottom:'1px solid #F4F1E8',
                fontSize:13, color: p.rare ? '#9A2B14' : '#0F0F0E',
                display:'flex', alignItems:'baseline', justifyContent:'space-between',
                gap:10,
              }}>
                <span style={{flex:1, minWidth:0}}>{p.name}</span>
                <span style={{
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:12, fontWeight:500, flex:'0 0 auto',
                }}>{p.odds}</span>
                <span style={{
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:11, color:'#6B6757', flex:'0 0 auto',
                  width:90, textAlign:'right',
                }}>{p.per}</span>
              </div>
            ))}
          </div>
        )}

        {tab === 'Inserts' && (
          <div>
            {window.INSERTS.map(p => (
              <div key={p.name} style={{
                padding:'10px 4px', borderBottom:'1px solid #F4F1E8',
                fontSize:13, display:'flex', justifyContent:'space-between', gap:10,
              }}>
                <span style={{flex:1, minWidth:0}}>{p.name}</span>
                <span style={{
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:12, fontWeight:500,
                }}>{p.odds}</span>
                <span style={{
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:11, color:'#6B6757', width:90, textAlign:'right',
                }}>{p.per}</span>
              </div>
            ))}
          </div>
        )}

        {tab === 'Autographs' && (
          <div>
            {window.AUTOGRAPHS.map(p => (
              <div key={p.name} style={{
                padding:'10px 4px', borderBottom:'1px solid #F4F1E8', fontSize:13,
                color: p.rare ? '#9A2B14' : '#0F0F0E',
              }}>
                <div style={{display:'flex', justifyContent:'space-between', gap:10}}>
                  <span style={{flex:1, minWidth:0}}>{p.name}</span>
                  <span style={{
                    fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                    fontSize:12, fontWeight:500,
                  }}>{p.odds}</span>
                </div>
                <div style={{
                  display:'flex', justifyContent:'space-between', marginTop:2,
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:11, color:'#6B6757',
                }}>
                  <span>{p.numbered}</span>
                  <span>{p.per}</span>
                </div>
              </div>
            ))}
          </div>
        )}
        <div style={{height:40}}/>
      </main>

      {/* DRAWER — 100% w × h overlay when open */}
      {drawerOpen && (
        <div style={{
          position:'absolute', inset:0, zIndex:100,
          background:'#FAFAF7',
          display:'flex', flexDirection:'column',
          paddingTop:54, // safe area for status bar
        }}>
          {/* Drawer header */}
          <div style={{
            padding:'14px 16px', borderBottom:'1px solid #EDEAE0',
            display:'flex', alignItems:'center', gap:12, background:'#FFFFFF',
          }}>
            <button onClick={()=>setDrawerOpen(false)} aria-label="Close" style={{
              background:'transparent', border:'none', cursor:'pointer',
              padding:4, display:'flex',
            }}>
              <IconX size={18}/>
            </button>
            <div style={{
              fontFamily:'"Inter Tight", sans-serif',
              fontSize:17, fontWeight:600, letterSpacing:-0.3,
            }}>Athletes in Set</div>
            <span style={{flex:1}}/>
            <span style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:11, color:'#8A8677',
            }}>{s.athletes}</span>
          </div>
          {/* Drawer body */}
          <div style={{flex:1, overflowY:'auto', padding:'14px 16px 30px'}}>
            <div style={{
              background:'#F1EFE9', borderRadius:10, padding:'9px 12px',
              display:'flex', alignItems:'center', gap:8, marginBottom:12,
            }}>
              <IconSearch size={15}/>
              <input placeholder="Search athletes…" style={{
                flex:1, border:'none', background:'transparent', outline:'none',
                fontSize:14, fontFamily:'inherit', color:'#0F0F0E',
              }}/>
            </div>
            <div style={{
              display:'flex', gap:6, flexWrap:'wrap', marginBottom:10,
            }}>
              {athleteFilters.map(f => {
                const active = f === athleteFilter;
                return (
                  <button key={f} onClick={()=>setAthleteFilter(f)} style={{
                    padding:'5px 11px', borderRadius:999, fontSize:12, fontWeight:500,
                    fontFamily:'inherit', cursor:'pointer',
                    background: active ? '#0F0F0E' : '#FFFFFF',
                    color: active ? '#FAFAF7' : '#3A372F',
                    border: active ? '1px solid #0F0F0E' : '1px solid #E6E3D9',
                  }}>{f}</button>
                );
              })}
            </div>
            <label style={{
              display:'inline-flex', alignItems:'center', gap:6,
              fontSize:12, color:'#3A372F', marginBottom:14,
            }}>
              <input type="checkbox" style={{accentColor:'#0F0F0E'}}/>
              Rookies only
            </label>
            <div style={{
              display:'flex', justifyContent:'space-between',
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:9, letterSpacing:1.6, color:'#8A8677', fontWeight:600,
              padding:'8px 4px', borderBottom:'1px solid #EDEAE0',
            }}>
              <span>ATHLETE</span><span>TOTAL CARDS</span>
            </div>
            {window.ATHLETES.map(a => (
              <div key={a.rank} style={{
                display:'flex', alignItems:'center', gap:12,
                padding:'12px 4px', borderBottom:'1px solid #F4F1E8',
              }}>
                <span style={{
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:11, color:'#8A8677', width:20,
                }}>{a.rank}</span>
                <div style={{
                  width:34, height:34, borderRadius:'50%', background:'#EAE6D9',
                  flex:'0 0 auto', display:'flex', alignItems:'center', justifyContent:'center',
                  fontSize:11, fontWeight:600, color:'#6B6757',
                }}>{a.name.split(' ').map(p=>p[0]).join('').slice(0,2)}</div>
                <div style={{flex:1, minWidth:0}}>
                  <div style={{display:'flex', alignItems:'center', gap:5}}>
                    <span style={{fontSize:14, fontWeight:600}}>{a.name}</span>
                    {a.rookie && <span style={{
                      fontSize:9, fontWeight:700, padding:'1px 4px', borderRadius:2,
                      background:'oklch(0.55 0.17 25)', color:'#FFF8F1', letterSpacing:0.6,
                    }}>RC</span>}
                  </div>
                  <div style={{fontSize:12, color:'#6B6757', marginTop:1}}>{a.team}</div>
                </div>
                <span style={{
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:14, fontWeight:600, color:'#0F0F0E',
                }}>{a.totalCards}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

window.OptionDMobile = OptionDMobile;

// Variant that mounts with drawer already open — for the canvas review.
function OptionDMobileOpen() {
  // Re-use OptionDMobile but force initial drawer-open via a key+ref trick:
  // simplest is to render OptionDMobile with a wrapper that auto-clicks the
  // Athletes button after mount.
  const ref = React.useRef(null);
  React.useEffect(() => {
    const btn = ref.current && ref.current.querySelector('button[aria-label="Athletes"]');
    if (btn) btn.click();
  }, []);
  return <div ref={ref} style={{width:'100%', height:'100%'}}><OptionDMobile/></div>;
}
window.OptionDMobileOpen = OptionDMobileOpen;
