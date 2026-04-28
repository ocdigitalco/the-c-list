// Option D — Hybrid of A + B (revised)
// Two-column outer layout from the top of the viewport down:
//   Left rail (300px): "Athletes in Set" — runs top-to-bottom, sticky.
//   Right column: hero + 6-stat ticker + primary tabs + content table.
// Tabs and stats live INSIDE the right column so they align with the data.
// Exclusive notes are layered inline under their relevant box-type rows.

function OptionD() {
  const s = window.SET_DETAIL;
  const [tab, setTab] = React.useState('Box Config');
  const [boxTab, setBoxTab] = React.useState('Hobby');
  const [athleteFilter, setAthleteFilter] = React.useState('Total Cards');
  const tabs = ['Box Config', 'Pack Odds', 'Inserts', 'Autographs'];
  const athleteFilters = ['Total Cards', 'Autographs', 'Inserts', 'Numbered'];

  // Map box types → exclusive notes (placeholder mapping; real schema would join)
  const boxExclusives = {
    Hobby:  ['Exclusive Red, White, and Blue Refractors'],
    Jumbo:  ['Exclusive Hot Pink and Lime Green X-Fractors'],
    Mega:   ['Exclusive Pulsar Refractors'],
  };

  return (
    <div style={{
      width:1280, background:'#FAFAF7', color:'#0F0F0E',
      fontFamily:'Inter, system-ui, sans-serif',
      display:'grid', gridTemplateColumns:'300px 1fr', alignItems:'stretch',
      borderTop:'1px solid #EDEAE0',
    }}>
      {/* LEFT — Athletes rail, full height from top */}
      <aside style={{
        borderRight:'1px solid #EDEAE0', background:'#FFFFFF',
        padding:'22px 18px',
      }}>
        <div style={{
          fontFamily:'"Inter Tight", Inter, sans-serif',
          fontSize:15, fontWeight:600, letterSpacing:-0.2, marginBottom:12,
        }}>Athletes in Set</div>
        <div style={{
          background:'#F1EFE9', borderRadius:8, padding:'7px 10px',
          display:'flex', alignItems:'center', gap:8, marginBottom:10,
        }}>
          <IconSearch size={14}/>
          <input placeholder="Search athletes…" style={{
            flex:1, border:'none', background:'transparent', outline:'none',
            fontSize:13, fontFamily:'inherit', color:'#0F0F0E',
          }}/>
        </div>
        <div style={{display:'flex', gap:4, flexWrap:'wrap', marginBottom:10}}>
          {athleteFilters.map(f => {
            const active = f === athleteFilter;
            return (
              <button key={f} onClick={()=>setAthleteFilter(f)} style={{
                padding:'4px 9px', borderRadius:4, fontSize:11, fontWeight:500,
                fontFamily:'inherit', cursor:'pointer',
                background: active ? '#0F0F0E' : 'transparent',
                color: active ? '#FAFAF7' : '#3A372F',
                border: active ? '1px solid #0F0F0E' : '1px solid #E6E3D9',
              }}>{f}</button>
            );
          })}
        </div>
        <label style={{
          display:'inline-flex', alignItems:'center', gap:6,
          fontSize:11, color:'#3A372F', marginBottom:14,
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
            display:'flex', alignItems:'center', gap:10,
            padding:'10px 4px', borderBottom:'1px solid #F4F1E8',
          }}>
            <span style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:11, color:'#8A8677', width:18,
            }}>{a.rank}</span>
            <div style={{
              width:30, height:30, borderRadius:'50%', background:'#EAE6D9',
              flex:'0 0 auto', display:'flex', alignItems:'center', justifyContent:'center',
              fontSize:10, fontWeight:600, color:'#6B6757',
            }}>{a.name.split(' ').map(p=>p[0]).join('').slice(0,2)}</div>
            <div style={{flex:1, minWidth:0}}>
              <div style={{display:'flex', alignItems:'center', gap:5}}>
                <span style={{fontSize:13, fontWeight:600, color:'#0F0F0E'}}>{a.name}</span>
                {a.rookie && <span style={{
                  fontSize:8, fontWeight:700, padding:'1px 4px', borderRadius:2,
                  background:'oklch(0.55 0.17 25)', color:'#FFF8F1', letterSpacing:0.6,
                }}>RC</span>}
              </div>
              <div style={{fontSize:11, color:'#6B6757', marginTop:1}}>{a.team}</div>
            </div>
            <span style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:13, fontWeight:600, color:'#0F0F0E',
            }}>{a.totalCards}</span>
          </div>
        ))}
      </aside>

      {/* RIGHT — hero, stats, tabs, content */}
      <div>
        {/* HERO */}
        <div style={{
          background:'#FFFFFF', borderBottom:'1px solid #EDEAE0',
          padding:'30px 36px',
          display:'grid', gridTemplateColumns:'140px 1fr 280px', gap:32, alignItems:'center',
        }}>
          <div style={{
            aspectRatio:'2/2.8', background:'linear-gradient(150deg, #C2102E 0%, #6B0A1B 100%)',
            position:'relative', overflow:'hidden', height:172, width:122,
            boxShadow:'0 12px 28px rgba(15,15,14,0.18)',
            transform:'rotate(-3deg)',
          }}>
            <div style={{position:'absolute', top:10, left:10, right:10,
              fontSize:9, fontWeight:700, color:'#FFF', letterSpacing:1.5,
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            }}>PATRIOTS</div>
            <div style={{position:'absolute', bottom:12, left:12, color:'#FFF'}}>
              <div style={{fontSize:14, fontWeight:700, fontFamily:'"Inter Tight", sans-serif'}}>DRAKE MAYE</div>
              <div style={{fontSize:9, opacity:0.85, marginTop:2, letterSpacing:1.2}}>QB · /5</div>
            </div>
          </div>
          <div>
            <div style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:10, letterSpacing:2.4, color:'#8A8677', fontWeight:600,
            }}>NFL · TOPPS · CHROME · {s.released.toUpperCase()}</div>
            <h1 style={{
              fontFamily:'"Inter Tight", Inter, sans-serif',
              fontSize:42, fontWeight:600, letterSpacing:-1.2,
              margin:'8px 0 12px', lineHeight:1.02, color:'#0F0F0E',
            }}>{s.name}</h1>
            <div style={{display:'flex', gap:6, alignItems:'center', flexWrap:'wrap'}}>
              <Chip>Football</Chip>
              <Chip>NFL</Chip>
              <Chip tone="dark">Chrome</Chip>
              <span style={{fontSize:12, color:'#6B6757', marginLeft:6}}>{s.athletes} athletes tracked</span>
            </div>
          </div>
          <div style={{
            background:'#FAFAF7', border:'1px solid #EDEAE0', borderRadius:8,
            padding:'12px 14px',
          }}>
            <div style={{
              display:'flex', justifyContent:'space-between', alignItems:'center',
              marginBottom:8,
            }}>
              <div style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:9, letterSpacing:1.6, color:'#8A8677', fontWeight:600,
              }}>COVERAGE</div>
              <button style={{
                padding:'5px 10px', background:'#0F0F0E', color:'#FAFAF7',
                border:'none', borderRadius:4, fontSize:10, fontWeight:600, cursor:'pointer',
                fontFamily:'inherit', letterSpacing:0.4,
              }}>↓ BREAK SHEET</button>
            </div>
            {[
              ['Athlete Checklist', s.coverage.athleteChecklist],
              ['Numbered Parallels', s.coverage.numberedParallels],
              ['Box Configuration', s.coverage.boxConfig],
              ['Pack Odds', s.coverage.packOdds],
            ].map(([k, ok]) => (
              <div key={k} style={{
                display:'flex', justifyContent:'space-between', alignItems:'center',
                padding:'4px 0', fontSize:11, color:'#3A372F',
              }}>
                <span>{k}</span>
                <span style={{
                  width:8, height:8, borderRadius:'50%',
                  background: ok ? '#0E8A4F' : '#B7B2A3',
                }}/>
              </div>
            ))}
          </div>
        </div>

        {/* STAT STRIP — spans right column */}
        <div style={{
          display:'grid', gridTemplateColumns:'repeat(6, 1fr)',
          background:'#FFFFFF', borderBottom:'1px solid #EDEAE0',
        }}>
          {[
            ['CARDS', s.cards.toLocaleString()],
            ['CARD TYPES', s.cardTypes],
            ['PARALLEL TYPES', s.parallelTypes],
            ['AUTOGRAPHS', s.autographs],
            ['AUTO PARALLELS', s.autoParallels.toLocaleString()],
            ['TOTAL PARALLELS', s.totalParallels.toLocaleString()],
          ].map(([label, val], i) => (
            <div key={label} style={{
              padding:'18px 22px',
              borderRight: i < 5 ? '1px solid #EDEAE0' : 'none',
            }}>
              <div style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:9, letterSpacing:1.6, color:'#8A8677', fontWeight:600,
              }}>{label}</div>
              <div style={{
                fontFamily:'"Inter Tight", Inter, sans-serif',
                fontSize:26, fontWeight:600, letterSpacing:-0.6, color:'#0F0F0E',
                marginTop:4,
              }}>{val}</div>
            </div>
          ))}
        </div>

        {/* PRIMARY TABS — aligned with content column */}
        <div style={{
          display:'flex', gap:0, padding:'0 36px',
          background:'#FAFAF7', borderBottom:'1px solid #EDEAE0',
        }}>
          {tabs.map(t => (
            <button key={t} onClick={()=>setTab(t)} style={{
              padding:'14px 20px', background:'none', border:'none',
              borderBottom: tab===t ? '2px solid #0F0F0E' : '2px solid transparent',
              marginBottom:-1, color: tab===t ? '#0F0F0E' : '#8A8677',
              fontFamily:'inherit', fontSize:13,
              fontWeight: tab===t ? 600 : 500, cursor:'pointer',
            }}>{t}</button>
          ))}
        </div>

        {/* CONTENT */}
        <main style={{padding:'28px 36px 60px'}}>
          {tab === 'Box Config' && (
            <div>
              <table style={{width:'100%', borderCollapse:'collapse', fontSize:13}}>
                <thead>
                  <tr style={{
                    fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                    fontSize:9, letterSpacing:1.6, color:'#6B6757', fontWeight:600,
                  }}>
                    <th style={{textAlign:'left', padding:'8px 10px', borderBottom:'1px solid #EDEAE0'}}>BOX TYPE</th>
                    <th style={{textAlign:'right', padding:'8px 10px', borderBottom:'1px solid #EDEAE0'}}>CARDS/PACK</th>
                    <th style={{textAlign:'right', padding:'8px 10px', borderBottom:'1px solid #EDEAE0'}}>PACKS/BOX</th>
                    <th style={{textAlign:'right', padding:'8px 10px', borderBottom:'1px solid #EDEAE0'}}>BOXES/CASE</th>
                    <th style={{textAlign:'right', padding:'8px 10px', borderBottom:'1px solid #EDEAE0'}}>PACKS/CASE</th>
                    <th style={{textAlign:'right', padding:'8px 10px', borderBottom:'1px solid #EDEAE0'}}>AUTOS/BOX</th>
                  </tr>
                </thead>
                <tbody>
                  {window.BOX_CONFIG.map(r => {
                    const exclusives = boxExclusives[r.type];
                    return (
                      <React.Fragment key={r.type}>
                        <tr>
                          <td style={{padding:'12px 10px', borderBottom: exclusives ? 'none' : '1px solid #F4F1E8', fontWeight:600}}>{r.type}</td>
                          <td style={{padding:'12px 10px', borderBottom: exclusives ? 'none' : '1px solid #F4F1E8', textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace'}}>{r.cardsPerPack}</td>
                          <td style={{padding:'12px 10px', borderBottom: exclusives ? 'none' : '1px solid #F4F1E8', textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace'}}>{r.packsPerBox}</td>
                          <td style={{padding:'12px 10px', borderBottom: exclusives ? 'none' : '1px solid #F4F1E8', textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace', color: r.boxesPerCase==null ? '#B7B2A3' : '#0F0F0E'}}>{r.boxesPerCase ?? '—'}</td>
                          <td style={{padding:'12px 10px', borderBottom: exclusives ? 'none' : '1px solid #F4F1E8', textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace', color: r.packsPerCase==null ? '#B7B2A3' : '#0F0F0E'}}>{r.packsPerCase ?? '—'}</td>
                          <td style={{padding:'12px 10px', borderBottom: exclusives ? 'none' : '1px solid #F4F1E8', textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace', color: r.autosPerBox==null ? '#B7B2A3' : '#0F0F0E'}}>{r.autosPerBox ?? '—'}</td>
                        </tr>
                        {exclusives && (
                          <tr>
                            <td colSpan={6} style={{
                              padding:'2px 10px 12px 10px',
                              borderBottom:'1px solid #F4F1E8',
                            }}>
                              {exclusives.map(n => (
                                <div key={n} style={{
                                  fontStyle:'italic', fontSize:12, color:'#6B6757',
                                }}>{n}</div>
                              ))}
                            </td>
                          </tr>
                        )}
                      </React.Fragment>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {tab === 'Pack Odds' && (
            <div>
              <div style={{display:'flex', gap:6, flexWrap:'wrap', marginBottom:18}}>
                {window.PACK_ODDS_TABS.map(t => {
                  const active = t === boxTab;
                  return (
                    <button key={t} onClick={()=>setBoxTab(t)} style={{
                      padding:'7px 12px', borderRadius:6, fontSize:12,
                      fontFamily:'inherit', fontWeight: active ? 600 : 500,
                      background: active ? '#0F0F0E' : '#FFFFFF',
                      color: active ? '#FAFAF7' : '#3A372F',
                      border: active ? '1px solid #0F0F0E' : '1px solid #EDEAE0',
                      cursor:'pointer',
                    }}>{t}</button>
                  );
                })}
              </div>
              <div style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:9, letterSpacing:1.6, color:'#6B6757', fontWeight:600,
                padding:'0 10px 8px', borderBottom:'1px solid #EDEAE0',
                display:'grid', gridTemplateColumns:'1fr 100px 160px',
              }}>
                <span>BASE PARALLELS</span>
                <span style={{textAlign:'right'}}>PACK ODDS</span>
                <span style={{textAlign:'right'}}>PER BOX (20 PACKS)</span>
              </div>
              {window.BASE_PARALLELS.map(p => (
                <div key={p.name} style={{
                  display:'grid', gridTemplateColumns:'1fr 100px 160px',
                  padding:'11px 10px', borderBottom:'1px solid #F4F1E8',
                  fontSize:13, color: p.rare ? '#9A2B14' : '#0F0F0E',
                }}>
                  <span>{p.name}</span>
                  <span style={{textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace'}}>{p.odds}</span>
                  <span style={{textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace', color:'#6B6757'}}>{p.per}</span>
                </div>
              ))}
            </div>
          )}

          {tab === 'Inserts' && (
            <div>
              <div style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:9, letterSpacing:1.6, color:'#6B6757', fontWeight:600,
                padding:'0 10px 8px', borderBottom:'1px solid #EDEAE0',
                display:'grid', gridTemplateColumns:'1fr 100px 160px',
              }}>
                <span>INSERT</span>
                <span style={{textAlign:'right'}}>PACK ODDS</span>
                <span style={{textAlign:'right'}}>PER BOX (20 PACKS)</span>
              </div>
              {window.INSERTS.map(p => (
                <div key={p.name} style={{
                  display:'grid', gridTemplateColumns:'1fr 100px 160px',
                  padding:'11px 10px', borderBottom:'1px solid #F4F1E8', fontSize:13,
                }}>
                  <span>{p.name}</span>
                  <span style={{textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace'}}>{p.odds}</span>
                  <span style={{textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace', color:'#6B6757'}}>{p.per}</span>
                </div>
              ))}
            </div>
          )}

          {tab === 'Autographs' && (
            <div>
              <div style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:9, letterSpacing:1.6, color:'#6B6757', fontWeight:600,
                padding:'0 10px 8px', borderBottom:'1px solid #EDEAE0',
                display:'grid', gridTemplateColumns:'1fr 70px 100px 160px',
              }}>
                <span>AUTOGRAPH</span>
                <span style={{textAlign:'right'}}>NUMBERED</span>
                <span style={{textAlign:'right'}}>PACK ODDS</span>
                <span style={{textAlign:'right'}}>PER BOX</span>
              </div>
              {window.AUTOGRAPHS.map(p => (
                <div key={p.name} style={{
                  display:'grid', gridTemplateColumns:'1fr 70px 100px 160px',
                  padding:'11px 10px', borderBottom:'1px solid #F4F1E8', fontSize:13,
                  color: p.rare ? '#9A2B14' : '#0F0F0E',
                }}>
                  <span>{p.name}</span>
                  <span style={{textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace', color:'#6B6757'}}>{p.numbered}</span>
                  <span style={{textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace'}}>{p.odds}</span>
                  <span style={{textAlign:'right', fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace', color:'#6B6757'}}>{p.per}</span>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

window.OptionD = OptionD;
