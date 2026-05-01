// Athlete Detail — Mobile (iOS)
// Mobile companion to AthleteDetailD. Same content adapted to a narrow viewport:
//   - Sticky compact app bar with hamburger that opens the Athletes drawer
//   - Hero: square photo + identity + chips
//   - Team Details summary card
//   - 4 stat tiles (2×2)
//   - Sticky horizontal-scroll tabs: Overview / Card Types / Base Parallels / Autographs
//   - Overview: Break Hit Calculator + Card Types list + Autographs list + Also Appears In
//   - Card Types: same accordion list (full-width)
//   - Base Parallels: condensed table with print run / odds / per-box
//   - Autographs: grouped flat table (set header rows + parallel rows)

function AthleteDetailDMobile() {
  const a = window.ATHLETE_DETAIL;
  const td = window.TEAM_DETAILS;
  const calc = window.BREAK_HIT_CALC;
  const [tab, setTab] = React.useState('Overview');
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [openSet, setOpenSet] = React.useState('Image Variations');
  const [openInsert, setOpenInsert] = React.useState('Power Players');
  const [athleteFilter, setAthleteFilter] = React.useState('Total Cards');
  const [team, setTeam] = React.useState('All Teams');
  const [cases, setCases] = React.useState(calc.cases);
  const [boxes, setBoxes] = React.useState(calc.boxes);
  const tabs = window.ATHLETE_TABS;
  const athleteFilters = ['Total Cards', 'Autographs', 'Inserts', 'Numbered'];
  const teams = React.useMemo(() => {
    const set = new Set(window.ATHLETES.map(at => at.team));
    return ['All Teams', ...Array.from(set).sort()];
  }, []);

  return (
    <div style={{
      width: '100%', minHeight: '100%', background: '#FAFAF7',
      color: '#0F0F0E', fontFamily: 'Inter, system-ui, sans-serif',
      paddingTop: 54,
      position: 'relative',
    }}>
      {/* APP TOP BAR — sticky */}
      <div style={{
        position: 'sticky', top: 54, zIndex: 10,
        background: 'rgba(250,250,247,0.92)',
        backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',
        borderBottom: '1px solid #EDEAE0',
        padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 10,
      }}>
        <button onClick={() => setDrawerOpen(true)} aria-label="Athletes" style={{
          background: '#FFFFFF', border: '1px solid #E6E3D9', borderRadius: 8,
          padding: '8px 10px', display: 'flex', alignItems: 'center', gap: 6,
          fontSize: 12, fontWeight: 500, color: '#3A372F', cursor: 'pointer',
          fontFamily: 'inherit',
        }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <circle cx="9" cy="8" r="3.2" stroke="#3A372F" strokeWidth="1.6"/>
            <circle cx="17" cy="9" r="2.4" stroke="#3A372F" strokeWidth="1.6"/>
            <path d="M3.5 18c.6-2.6 2.7-4.2 5.5-4.2s4.9 1.6 5.5 4.2" stroke="#3A372F" strokeWidth="1.6" strokeLinecap="round"/>
            <path d="M15 16c.4-1.4 1.5-2.4 3-2.4 1.5 0 2.6 1 3 2.4" stroke="#3A372F" strokeWidth="1.6" strokeLinecap="round"/>
          </svg>
          Athletes
        </button>
        <a href={a.setHref} style={{
          flex: 1, minWidth: 0,
          fontSize: 11, color: '#6B6757', textDecoration: 'none',
          display: 'inline-flex', alignItems: 'center', gap: 4,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>
          <IconChev dir="left" size={11} color="#6B6757"/>
          <span style={{
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          }}>{a.setName}</span>
        </a>
      </div>

      {/* HERO */}
      <div style={{
        padding: '16px 14px 14px', background: '#FFFFFF',
        borderBottom: '1px solid #EDEAE0',
      }}>
        <div style={{ display: 'flex', gap: 14, alignItems: 'flex-start' }}>
          <AthletePhotoMobile name={a.name} team={a.teamShort} src={a.photoUrl}/>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
            }}>{a.position} · #{a.jersey} · {a.team.toUpperCase()}</div>
            <h1 style={{
              fontFamily: '"Inter Tight", Inter, sans-serif',
              fontSize: 24, fontWeight: 600, letterSpacing: -0.6,
              margin: '4px 0 8px', lineHeight: 1.05, color: '#0F0F0E',
            }}>{a.name}</h1>
            <div style={{ display: 'flex', gap: 5, alignItems: 'center', flexWrap: 'wrap' }}>
              <Chip>NFL</Chip>
              <Chip tone="dark">Chrome</Chip>
            </div>
          </div>
        </div>
      </div>

      {/* STAT GRID — single row of 4 */}
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
        background: '#FFFFFF', borderBottom: '1px solid #EDEAE0',
      }}>
        {[
          ['CARD TYPES', a.cardTypes.toString()],
          ['TOTAL CARDS', a.totalCards.toLocaleString()],
          ['NUMBERED', a.numberedParallels.toLocaleString()],
          ['1/1S', a.oneOfOnes.toString()],
        ].map(([label, val], i) => (
          <div key={label} style={{
            padding: '12px 10px',
            borderRight: i < 3 ? '1px solid #EDEAE0' : 'none',
            minWidth: 0,
          }}>
            <div style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 8, letterSpacing: 1.2, color: '#8A8677', fontWeight: 600,
              whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
            }}>{label}</div>
            <div style={{
              fontFamily: '"Inter Tight", Inter, sans-serif',
              fontSize: 18, fontWeight: 600, letterSpacing: -0.5, color: '#0F0F0E',
              marginTop: 3, whiteSpace: 'nowrap',
            }}>{val}</div>
          </div>
        ))}
      </div>

      {/* TABS — sticky, horizontal scroll */}
      <div style={{
        position: 'sticky', top: 54 + 41, zIndex: 9,
        display: 'flex', gap: 0, padding: '0 14px',
        background: '#FAFAF7', borderBottom: '1px solid #EDEAE0',
        overflowX: 'auto', WebkitOverflowScrolling: 'touch',
      }}>
        {tabs.map(t => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: '12px 12px', background: 'none', border: 'none',
            borderBottom: tab === t ? '2px solid #0F0F0E' : '2px solid transparent',
            marginBottom: -1, color: tab === t ? '#0F0F0E' : '#8A8677',
            fontFamily: 'inherit', fontSize: 13, whiteSpace: 'nowrap',
            fontWeight: tab === t ? 600 : 500, cursor: 'pointer',
          }}>{t}</button>
        ))}
      </div>

      {/* CONTENT */}
      <main style={{ padding: '14px' }}>
        {tab === 'Overview' && (
          <>
            {/* Break Hit Calculator (flipped above team details, flush stack) */}
            <BreakCalcMobile calc={calc} cases={cases} boxes={boxes} setCases={setCases} setBoxes={setBoxes} flush="top"/>
            <TeamDetailsMobile td={td} flush="bottom"/>

            <SectionHeadMobile>Card Types</SectionHeadMobile>
            <AccordionListMobile
              items={window.INSERT_SETS}
              openName={openSet}
              onToggle={(n) => setOpenSet(openSet === n ? null : n)}/>

            <SectionHeadMobile>Autographs</SectionHeadMobile>
            <GroupedTableMobile items={window.AUTOGRAPH_SETS} heading="AUTO PARALLELS"/>
          </>
        )}

        {tab === 'Card Types' && (
          <AccordionListMobile
            items={window.INSERT_SETS}
            openName={openSet}
            onToggle={(n) => setOpenSet(openSet === n ? null : n)}/>
        )}

        {tab === 'Inserts' && (
          <GroupedTableMobile items={window.INSERT_TABLE} heading="INSERT PARALLELS"/>
        )}

        {tab === 'Base Parallels' && (
          <ParallelsTableMobile/>
        )}

        {tab === 'Autographs' && (
          <GroupedTableMobile items={window.AUTOGRAPH_SETS} heading="AUTO PARALLELS"/>
        )}

        {tab === 'Also Featured In' && (
          <AlsoFeaturedInMobile/>
        )}
        <div style={{ height: 40 }}/>
      </main>

      {/* DRAWER — full-screen overlay when open */}
      {drawerOpen && (
        <div style={{
          position: 'absolute', inset: 0, zIndex: 100,
          background: '#FAFAF7',
          display: 'flex', flexDirection: 'column',
          paddingTop: 54,
        }}>
          <div style={{
            padding: '14px 16px', borderBottom: '1px solid #EDEAE0',
            display: 'flex', alignItems: 'center', gap: 12, background: '#FFFFFF',
          }}>
            <button onClick={() => setDrawerOpen(false)} aria-label="Close" style={{
              background: 'transparent', border: 'none', cursor: 'pointer',
              padding: 4, display: 'flex',
            }}>
              <IconX size={18}/>
            </button>
            <div style={{
              fontFamily: '"Inter Tight", sans-serif',
              fontSize: 17, fontWeight: 600, letterSpacing: -0.3,
            }}>Athletes in Set</div>
            <span style={{ flex: 1 }}/>
            <span style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 11, color: '#8A8677',
            }}>{window.ATHLETES.length}</span>
          </div>
          <div style={{ flex: 1, overflowY: 'auto', padding: '14px 16px 30px' }}>
            <div style={{
              background: '#F1EFE9', borderRadius: 10, padding: '9px 12px',
              display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12,
            }}>
              <IconSearch size={15}/>
              <input placeholder="Search athletes…" style={{
                flex: 1, border: 'none', background: 'transparent', outline: 'none',
                fontSize: 14, fontFamily: 'inherit', color: '#0F0F0E',
              }}/>
            </div>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 10 }}>
              {athleteFilters.map(f => {
                const active = f === athleteFilter;
                return (
                  <button key={f} onClick={() => setAthleteFilter(f)} style={{
                    padding: '5px 11px', borderRadius: 999, fontSize: 12, fontWeight: 500,
                    fontFamily: 'inherit', cursor: 'pointer',
                    background: active ? '#0F0F0E' : '#FFFFFF',
                    color: active ? '#FAFAF7' : '#3A372F',
                    border: active ? '1px solid #0F0F0E' : '1px solid #E6E3D9',
                  }}>{f}</button>
                );
              })}
            </div>
            <div style={{ marginBottom: 12 }}>
              <div style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
                marginBottom: 6,
              }}>TEAM</div>
              <div style={{
                position: 'relative',
                border: '1px solid #E6E3D9', borderRadius: 8, background: '#FFFFFF',
              }}>
                <select value={team} onChange={e => setTeam(e.target.value)} style={{
                  width: '100%', appearance: 'none', WebkitAppearance: 'none',
                  background: 'transparent', border: 'none', outline: 'none',
                  padding: '9px 30px 9px 12px', fontSize: 13, fontFamily: 'inherit',
                  color: '#0F0F0E', cursor: 'pointer',
                }}>
                  {teams.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
                <span style={{
                  position: 'absolute', right: 12, top: '50%',
                  transform: 'translateY(-50%)', pointerEvents: 'none',
                  display: 'inline-flex',
                }}>
                  <IconChev dir="down" size={11} color="#6B6757"/>
                </span>
              </div>
            </div>
            <label style={{
              display: 'inline-flex', alignItems: 'center', gap: 6,
              fontSize: 12, color: '#3A372F', marginBottom: 14,
            }}>
              <input type="checkbox" style={{ accentColor: '#0F0F0E' }}/>
              Rookies only
            </label>
            <div style={{
              display: 'flex', justifyContent: 'space-between',
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
              padding: '8px 4px', borderBottom: '1px solid #EDEAE0',
            }}>
              <span>ATHLETE</span><span>TOTAL CARDS</span>
            </div>
            {window.ATHLETES.map(at => {
              const selected = at.name === a.name;
              return (
                <div key={at.rank} style={{
                  display: 'flex', alignItems: 'center', gap: 12,
                  padding: '12px 8px', borderBottom: '1px solid #F4F1E8',
                  background: selected ? '#F4F1E8' : 'transparent',
                  borderLeft: selected ? '2px solid #0F0F0E' : '2px solid transparent',
                  marginLeft: selected ? -8 : 0, paddingLeft: selected ? 14 : 4,
                }}>
                  <span style={{
                    fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                    fontSize: 11, color: '#8A8677', width: 20,
                  }}>{at.rank}</span>
                  <div style={{
                    width: 34, height: 34, borderRadius: '50%',
                    background: selected ? '#0F0F0E' : '#EAE6D9',
                    color: selected ? '#FAFAF7' : '#6B6757',
                    flex: '0 0 auto', display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 11, fontWeight: 600,
                  }}>{at.name.split(' ').map(p => p[0]).join('').slice(0, 2)}</div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                      <span style={{ fontSize: 14, fontWeight: 600 }}>{at.name}</span>
                      {at.rookie && <span style={{
                        fontSize: 9, fontWeight: 700, padding: '1px 4px', borderRadius: 2,
                        background: 'oklch(0.55 0.17 25)', color: '#FFF8F1', letterSpacing: 0.6,
                      }}>RC</span>}
                    </div>
                    <div style={{ fontSize: 12, color: '#6B6757', marginTop: 1 }}>{at.team}</div>
                  </div>
                  <span style={{
                    fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                    fontSize: 14, fontWeight: 600, color: '#0F0F0E',
                  }}>{at.totalCards}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Mobile sub-components ───────────────────────────────────────────────

function AthletePhotoMobile({ name, team, src }) {
  const initials = name.split(' ').map(p => p[0]).join('').slice(0, 2);
  return (
    <div style={{
      width: 96, height: 96, position: 'relative', flex: '0 0 auto',
      background: '#F1EFE9', border: '1px solid #EDEAE0',
      overflow: 'hidden',
    }}>
      {src ? (
        <img src={src} alt={name} style={{
          width: '100%', height: '100%', objectFit: 'cover', display: 'block',
        }}/>
      ) : (
        <>
          <div style={{
            position: 'absolute', inset: 0,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: '"Inter Tight", Inter, sans-serif',
            fontSize: 36, fontWeight: 600, letterSpacing: -1,
            color: '#C4BEAD',
          }}>{initials}</div>
          <div style={{
            position: 'absolute', top: 6, left: 6,
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize: 7, letterSpacing: 1.4, color: '#8A8677', fontWeight: 600,
          }}>PHOTO</div>
        </>
      )}
    </div>
  );
}

function TeamDetailsMobile({ td, flush }) {
  // flush="bottom" → squared top edge, no top border, no bottom margin gap
  const flushStyle = flush === 'bottom' ? {
    borderRadius: 0,
    borderTop: 'none',
    marginBottom: 14,
  } : flush === 'top' ? {
    borderRadius: 0,
    borderBottom: 'none',
    marginBottom: 0,
  } : {};
  return (
    <div style={{
      background: '#FFFFFF', border: '1px solid #EDEAE0', borderRadius: 10,
      padding: '14px 14px', marginBottom: 14,
      ...flushStyle,
    }}>
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        marginBottom: 8,
      }}>
        <div style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
        }}>TEAM DETAILS</div>
        <a href="#" style={{
          fontSize: 10, color: '#3A372F', textDecoration: 'none',
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          letterSpacing: 0.6, fontWeight: 600,
        }}>VIEW TEAM →</a>
      </div>
      <div style={{
        fontFamily: '"Inter Tight", Inter, sans-serif',
        fontSize: 15, fontWeight: 600, letterSpacing: -0.2, color: '#0F0F0E',
        marginBottom: 8,
      }}>{td.team}</div>
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', rowGap: 4, columnGap: 16,
      }}>
        {[
          ['Athletes in set', td.athletesInSet],
          ['Total cards', td.totalCards.toLocaleString()],
          ['Autographs', td.autographs],
          ['Rookies', td.rookies],
          ['Numbered parallels', td.numberedParallels.toLocaleString()],
        ].map(([k, v]) => (
          <div key={k} style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            fontSize: 11, color: '#3A372F', padding: '3px 0',
          }}>
            <span style={{ color: '#6B6757' }}>{k}</span>
            <span style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontWeight: 600, color: '#0F0F0E',
            }}>{v}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function BreakCalcMobile({ calc, cases, boxes, setCases, setBoxes, flush }) {
  // flush="top" → squared bottom edge, no bottom border, 0 bottom margin so
  // it sits flush against the card below.
  const flushStyle = flush === 'top' ? {
    borderRadius: 0,
    borderBottom: 'none',
    marginBottom: 0,
  } : flush === 'bottom' ? {
    borderRadius: 0,
    borderTop: 'none',
    marginBottom: 14,
  } : {};
  return (
    <div style={{
      background: '#FFFFFF', border: '1px solid #EDEAE0', borderRadius: 10,
      padding: '14px 14px', marginBottom: 14,
      ...flushStyle,
    }}>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
      }}>BREAK HIT CALCULATOR</div>
      <div style={{
        fontFamily: '"Inter Tight", Inter, sans-serif',
        fontSize: 15, fontWeight: 600, letterSpacing: -0.2, color: '#0F0F0E',
        marginTop: 4, marginBottom: 12,
      }}>How likely is Drake Maye in your break?</div>
      <div style={{ display: 'flex', gap: 10, marginBottom: 8 }}>
        <StepperMobile label="CASES" value={cases} onChange={setCases}/>
        <StepperMobile label="BOXES" value={boxes} onChange={setBoxes}/>
      </div>
      {calc.rows.map(r => {
        const dot = r.tone === 'good' ? '#0E8A4F' : r.tone === 'medium' ? '#C28A18' : '#9A2B14';
        return (
          <div key={r.label} style={{
            display: 'grid', gridTemplateColumns: '14px 1fr auto',
            alignItems: 'center', gap: 10,
            padding: '10px 0', borderTop: '1px solid #F4F1E8',
          }}>
            <span style={{
              width: 8, height: 8, borderRadius: '50%', background: dot, justifySelf: 'center',
            }}/>
            <div>
              <div style={{ fontSize: 13, fontWeight: 600, color: '#0F0F0E' }}>{r.label}</div>
              <div style={{ fontSize: 11, color: '#6B6757', marginTop: 1 }}>{r.sub}</div>
            </div>
            <div style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 14, fontWeight: 600, color: dot, textAlign: 'right',
            }}>{r.odds}</div>
          </div>
        );
      })}
      <div style={{
        marginTop: 10, padding: '8px 10px', background: '#FAFAF7', borderRadius: 6,
        fontSize: 10, color: '#8A8677',
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace', letterSpacing: 0.4,
      }}>
        {cases} CASE{cases !== 1 ? 'S' : ''} · {boxes} BOX{boxes !== 1 ? 'ES' : ''} · {boxes * 20} PACKS
      </div>
    </div>
  );
}

function StepperMobile({ label, value, onChange }) {
  const btn = {
    padding: '6px 12px', background: '#FFF', border: 'none', cursor: 'pointer',
    fontSize: 14, color: '#3A372F', fontFamily: 'inherit',
  };
  return (
    <div style={{ flex: 1 }}>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 8, letterSpacing: 1.4, color: '#8A8677', fontWeight: 600,
        marginBottom: 4,
      }}>{label}</div>
      <div style={{
        display: 'flex', alignItems: 'center',
        border: '1px solid #EDEAE0', borderRadius: 6, overflow: 'hidden',
      }}>
        <button onClick={() => onChange(Math.max(1, value - 1))} style={btn}>−</button>
        <div style={{
          flex: 1, textAlign: 'center', padding: '6px 0', fontSize: 13, fontWeight: 600,
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          borderLeft: '1px solid #EDEAE0', borderRight: '1px solid #EDEAE0', background: '#FFF',
        }}>{value}</div>
        <button onClick={() => onChange(value + 1)} style={btn}>+</button>
      </div>
    </div>
  );
}

function SectionHeadMobile({ children }) {
  return (
    <div style={{
      fontFamily: '"Inter Tight", Inter, sans-serif',
      fontSize: 15, fontWeight: 600, letterSpacing: -0.2, color: '#0F0F0E',
      margin: '20px 0 10px',
    }}>{children}</div>
  );
}

function AccordionListMobile({ items, openName, onToggle }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
      {items.map(s => {
        const open = s.name === openName;
        return (
          <div key={s.name} style={{
            border: open ? '1.5px solid #0F0F0E' : '1px solid #EDEAE0',
            borderRadius: 8, background: '#FFFFFF', overflow: 'hidden',
          }}>
            <button onClick={() => onToggle(s.name)} style={{
              width: '100%', padding: '12px 14px', display: 'flex',
              justifyContent: 'space-between', alignItems: 'center', gap: 8,
              background: 'transparent', border: 'none', cursor: 'pointer',
              fontFamily: 'inherit', textAlign: 'left',
            }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: '#0F0F0E' }}>{s.name}</div>
                <div style={{
                  fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize: 10, color: '#8A8677', marginTop: 2,
                }}>{s.cards} card{s.cards !== 1 ? 's' : ''} · {s.parallels} parallel{s.parallels !== 1 ? 's' : ''}</div>
              </div>
              <IconChev dir={open ? 'up' : 'down'} size={14} color="#3A372F"/>
            </button>
            {open && s.details && <AccordionDetailMobile d={s.details}/>}
          </div>
        );
      })}
    </div>
  );
}

function AccordionDetailMobile({ d }) {
  const toneMap = {
    silver: { bg: '#E6E3D9', fg: '#3A372F' },
    orange: { bg: '#F1D4B8', fg: '#7A3F0E' },
    teal:   { bg: '#BFE0DA', fg: '#15554C' },
    blue:   { bg: '#C8D3E8', fg: '#1F3A6A' },
    green:  { bg: '#C7DFC4', fg: '#1F4F22' },
    black:  { bg: '#3A372F', fg: '#FAFAF7' },
    red:    { bg: '#E8C2BD', fg: '#7A1A12' },
    gold:   { bg: '#F0D88A', fg: '#5A3F0A' },
  };
  return (
    <div style={{ padding: '0 14px 14px' }}>
      <div style={{
        display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'baseline',
        padding: '10px 0 12px', borderTop: '1px solid #F4F1E8',
      }}>
        <span style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 11, fontWeight: 600, color: '#0F0F0E',
          background: '#F1EFE9', padding: '3px 6px', borderRadius: 3,
        }}>{d.cardNumber}</span>
        <span style={{ fontSize: 13, fontWeight: 600, color: '#0F0F0E' }}>{d.subject}</span>
        <span style={{ fontSize: 11, color: '#6B6757' }}>{d.team}</span>
      </div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
        marginBottom: 8,
      }}>PARALLELS</div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
        {d.parallels.map(p => {
          const t = toneMap[p.tone] || toneMap.silver;
          return (
            <span key={p.name} style={{
              display: 'inline-flex', alignItems: 'baseline', gap: 6,
              padding: '5px 9px', borderRadius: 4, fontSize: 11, fontWeight: 500,
              background: t.bg, color: t.fg,
            }}>
              <span>{p.name}</span>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 10, opacity: 0.75,
              }}>{p.run}</span>
            </span>
          );
        })}
      </div>
    </div>
  );
}

function ParallelsTableMobile() {
  const cols = '1fr 56px 64px';
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 8, letterSpacing: 1.4, color: '#6B6757', fontWeight: 600,
        padding: '0 4px 8px', borderBottom: '1px solid #EDEAE0',
        display: 'grid', gridTemplateColumns: cols, gap: 8,
      }}>
        <span>BASE PARALLELS</span>
        <span style={{ textAlign: 'right' }}>RUN</span>
        <span style={{ textAlign: 'right' }}>ODDS</span>
      </div>
      {window.BASE_PARALLELS.map(p => (
        <div key={p.name} style={{
          display: 'grid', gridTemplateColumns: cols, gap: 8,
          padding: '10px 4px', borderBottom: '1px solid #F4F1E8',
          fontSize: 12, color: p.rare ? '#9A2B14' : '#0F0F0E', alignItems: 'baseline',
        }}>
          <span>{p.name}</span>
          <span style={{
            textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            color: p.run === 'unnumbered' ? '#B7B2A3' : (p.rare ? '#9A2B14' : '#0F0F0E'),
            fontWeight: p.run === 'unnumbered' ? 400 : 600, fontSize: 11,
          }}>{p.run === 'unnumbered' ? '—' : p.run}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize: 11,
          }}>{p.odds}</span>
        </div>
      ))}
    </div>
  );
}

function GroupedTableMobile({ items, heading }) {
  const cols = '1fr 56px 64px';
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 8, letterSpacing: 1.4, color: '#6B6757', fontWeight: 600,
        padding: '0 4px 8px', borderBottom: '1px solid #EDEAE0',
        display: 'grid', gridTemplateColumns: cols, gap: 8,
      }}>
        <span>{heading}</span>
        <span style={{ textAlign: 'right' }}>RUN</span>
        <span style={{ textAlign: 'right' }}>ODDS</span>
      </div>
      {items.map((s, si) => (
        <React.Fragment key={s.name}>
          <div style={{
            padding: si === 0 ? '12px 4px 8px' : '18px 4px 8px',
            borderBottom: '1px solid #EDEAE0',
          }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, flexWrap: 'wrap' }}>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 10, fontWeight: 600, color: '#0F0F0E',
                background: '#F1EFE9', padding: '2px 6px', borderRadius: 3,
              }}>{s.cardNumber}</span>
              <span style={{ fontSize: 13, fontWeight: 600, color: '#0F0F0E', letterSpacing: -0.1 }}>{s.name}</span>
            </div>
            <div style={{ fontSize: 11, color: '#6B6757', marginTop: 3 }}>{s.subject}</div>
          </div>
          {s.parallels.map(p => (
            <div key={s.name + p.name} style={{
              display: 'grid', gridTemplateColumns: cols, gap: 8,
              padding: '10px 4px', borderBottom: '1px solid #F4F1E8',
              fontSize: 12, color: p.rare ? '#9A2B14' : '#0F0F0E', alignItems: 'baseline',
            }}>
              <span>{p.name}</span>
              <span style={{
                textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 11, fontWeight: p.run === 'unnumbered' ? 400 : 600,
                color: p.run === 'unnumbered' ? '#B7B2A3' : (p.rare ? '#9A2B14' : '#0F0F0E'),
              }}>{p.run === 'unnumbered' ? '—' : p.run}</span>
              <span style={{
                textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 11, color: p.rare ? '#9A2B14' : '#3A372F',
              }}>{p.odds}</span>
            </div>
          ))}
        </React.Fragment>
      ))}
    </div>
  );
}

window.AthleteDetailDMobile = AthleteDetailDMobile;

function AlsoFeaturedInMobile() {
  return (
    <div>
      {window.ALSO_APPEARS_IN.map(s => (
        <a key={s.name} href="#" style={{
          display: 'block', textDecoration: 'none', color: 'inherit',
          background: '#FFFFFF', border: '1px solid #EDEAE0', borderRadius: 10,
          padding: '14px 14px', marginBottom: 8,
        }}>
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
            gap: 10, marginBottom: 8,
          }}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{
                fontSize: 14, fontWeight: 600, color: '#0F0F0E', letterSpacing: -0.1,
              }}>{s.name}</div>
              <div style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 10, color: '#8A8677', marginTop: 2, letterSpacing: 0.6,
              }}>{s.brand} · {s.sport} · {s.year}</div>
            </div>
            <span style={{ color: '#8A8677', fontSize: 16 }}>→</span>
          </div>
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
            borderTop: '1px solid #F4F1E8', paddingTop: 10,
          }}>
            {[
              ['HIS CARDS', s.cards],
              ['AUTOS', s.autos === 0 ? '—' : s.autos],
              ['PARALLELS', s.parallels],
            ].map(([k, v], i) => (
              <div key={k} style={{
                paddingLeft: i === 0 ? 0 : 10,
                borderLeft: i === 0 ? 'none' : '1px solid #F4F1E8',
              }}>
                <div style={{
                  fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize: 8, letterSpacing: 1.2, color: '#8A8677', fontWeight: 600,
                }}>{k}</div>
                <div style={{
                  fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize: 14, fontWeight: 600,
                  color: v === '—' ? '#B7B2A3' : '#0F0F0E',
                  marginTop: 2,
                }}>{v}</div>
              </div>
            ))}
          </div>
        </a>
      ))}
    </div>
  );
}

// Variant that mounts with drawer already open — for canvas review.
function AthleteDetailDMobileOpen() {
  const ref = React.useRef(null);
  React.useEffect(() => {
    const btn = ref.current && ref.current.querySelector('button[aria-label="Athletes"]');
    if (btn) btn.click();
  }, []);
  return <div ref={ref} style={{ width: '100%', height: '100%' }}><AthleteDetailDMobile/></div>;
}
window.AthleteDetailDMobileOpen = AthleteDetailDMobileOpen;
