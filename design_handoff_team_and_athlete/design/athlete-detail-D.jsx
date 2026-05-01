// Athlete Detail — adapts Option D's design language to a single-athlete view.
// Same outer shell as OptionD: 300px athletes rail + right column with hero,
// stat strip, primary tabs, and content. Drake Maye is the selected athlete
// (highlighted in the rail) and the right column shows his card, totals,
// break-hit calculator, and the insert / autograph sets he appears in.

function AthleteDetailD() {
  const a = window.ATHLETE_DETAIL;
  const calc = window.BREAK_HIT_CALC;
  const [tab, setTab] = React.useState('Overview');
  const [athleteFilter, setAthleteFilter] = React.useState('Total Cards');
  const [openSet, setOpenSet] = React.useState('Image Variations');
  const [openInsert, setOpenInsert] = React.useState('Power Players');
  const [openAuto, setOpenAuto] = React.useState('Veteran Auto');
  const [cases, setCases] = React.useState(calc.cases);
  const [boxes, setBoxes] = React.useState(calc.boxes);
  const tabs = window.ATHLETE_TABS;
  const athleteFilters = ['Total Cards', 'Autographs', 'Inserts', 'Numbered'];
  const teams = React.useMemo(() => {
    const set = new Set(window.ATHLETES.map((at) => at.team));
    return ['All Teams', ...Array.from(set).sort()];
  }, []);
  const [team, setTeam] = React.useState('All Teams');

  const initials = a.name.split(' ').map((p) => p[0]).join('').slice(0, 2);

  return (
    <div style={{
      width: 1280, background: '#FAFAF7', color: '#0F0F0E',
      fontFamily: 'Inter, system-ui, sans-serif',
      display: 'grid', gridTemplateColumns: '300px 1fr', alignItems: 'stretch',
      borderTop: '1px solid #EDEAE0'
    }}>
      {/* LEFT — Athletes rail */}
      <aside style={{
        borderRight: '1px solid #EDEAE0', background: '#FFFFFF',
        padding: '22px 18px'
      }}>
        <div style={{
          fontFamily: '"Inter Tight", Inter, sans-serif',
          fontSize: 15, fontWeight: 600, letterSpacing: -0.2, marginBottom: 12
        }}>Athletes in Set</div>
        <div style={{
          background: '#F1EFE9', borderRadius: 8, padding: '7px 10px',
          display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10
        }}>
          <IconSearch size={14} />
          <input placeholder="Search athletes…" style={{
            flex: 1, border: 'none', background: 'transparent', outline: 'none',
            fontSize: 13, fontFamily: 'inherit', color: '#0F0F0E'
          }} />
        </div>
        <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginBottom: 10 }}>
          {athleteFilters.map((f) => {
            const active = f === athleteFilter;
            return (
              <button key={f} onClick={() => setAthleteFilter(f)} style={{
                padding: '4px 9px', borderRadius: 4, fontSize: 11, fontWeight: 500,
                fontFamily: 'inherit', cursor: 'pointer',
                background: active ? '#0F0F0E' : 'transparent',
                color: active ? '#FAFAF7' : '#3A372F',
                border: active ? '1px solid #0F0F0E' : '1px solid #E6E3D9'
              }}>{f}</button>);

          })}
        </div>
        {/* Team filter */}
        <div style={{ marginBottom: 10 }}>
          <div style={{
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
            marginBottom: 6
          }}>TEAM</div>
          <div style={{
            position: 'relative',
            border: '1px solid #E6E3D9', borderRadius: 6,
            background: '#FFFFFF'
          }}>
            <select
              value={team}
              onChange={(e) => setTeam(e.target.value)}
              style={{
                width: '100%', appearance: 'none', WebkitAppearance: 'none',
                background: 'transparent', border: 'none', outline: 'none',
                padding: '7px 28px 7px 10px', fontSize: 12, fontFamily: 'inherit',
                color: '#0F0F0E', cursor: 'pointer'
              }}>
              {teams.map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
            <span style={{
              position: 'absolute', right: 10, top: '50%',
              transform: 'translateY(-50%)', pointerEvents: 'none',
              display: 'inline-flex'
            }}>
              <IconChev dir="down" size={11} color="#6B6757" />
            </span>
          </div>
        </div>
        <label style={{
          display: 'inline-flex', alignItems: 'center', gap: 6,
          fontSize: 11, color: '#3A372F', marginBottom: 14
        }}>
          <input type="checkbox" style={{ accentColor: '#0F0F0E' }} />
          Rookies only
        </label>
        <div style={{
          display: 'flex', justifyContent: 'space-between',
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
          padding: '8px 4px', borderBottom: '1px solid #EDEAE0'
        }}>
          <span>ATHLETE</span><span>TOTAL CARDS</span>
        </div>
        {window.ATHLETES.map((ath) => {
          const selected = ath.name === a.name;
          return (
            <div key={ath.rank} style={{
              display: 'flex', alignItems: 'center', gap: 10,
              padding: '10px 8px', borderBottom: '1px solid #F4F1E8',
              background: selected ? '#F4F1E8' : 'transparent',
              borderLeft: selected ? '2px solid #0F0F0E' : '2px solid transparent',
              marginLeft: selected ? -8 : 0, paddingLeft: selected ? 12 : 4,
              borderRadius: selected ? 0 : 0
            }}>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 11, color: '#8A8677', width: 18
              }}>{ath.rank}</span>
              <div style={{
                width: 30, height: 30, borderRadius: '50%', background: selected ? '#0F0F0E' : '#EAE6D9',
                flex: '0 0 auto', display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 10, fontWeight: 600, color: selected ? '#FAFAF7' : '#6B6757'
              }}>{ath.name.split(' ').map((p) => p[0]).join('').slice(0, 2)}</div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                  <span style={{ fontSize: 13, fontWeight: 600, color: '#0F0F0E' }}>{ath.name}</span>
                  {ath.rookie && <span style={{
                    fontSize: 8, fontWeight: 700, padding: '1px 4px', borderRadius: 2,
                    background: 'oklch(0.55 0.17 25)', color: '#FFF8F1', letterSpacing: 0.6
                  }}>RC</span>}
                </div>
                <div style={{ fontSize: 11, color: '#6B6757', marginTop: 1 }}>{ath.team}</div>
              </div>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 13, fontWeight: 600, color: '#0F0F0E'
              }}>{ath.totalCards}</span>
            </div>);

        })}
      </aside>

      {/* RIGHT — hero, stats, tabs, content */}
      <div>
        {/* HERO */}
        <div style={{
          background: '#FFFFFF', borderBottom: '1px solid #EDEAE0',
          padding: '22px 36px 28px'
        }}>
          {/* Breadcrumb */}
          <a href={a.setHref} style={{
            display: 'inline-flex', alignItems: 'center', gap: 6,
            fontSize: 12, color: '#6B6757', textDecoration: 'none', marginBottom: 18
          }}>
            <IconChev dir="left" size={12} color="#6B6757" />
            <span>{a.setName}</span>
          </a>

          <div style={{
            display: 'grid', gridTemplateColumns: '180px 1fr 280px',
            gap: 32, alignItems: 'center'
          }}>
            {/* Athlete photo — square slot, API-driven (placeholder shown) */}
            <AthletePhoto name={a.name} team={a.teamShort} src={a.photoUrl} />

            <div>
              <div style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 10, letterSpacing: 2.4, color: '#8A8677', fontWeight: 600
              }}>{a.position} · #{a.jersey} · {a.team.toUpperCase()}</div>
              <h1 style={{
                fontFamily: '"Inter Tight", Inter, sans-serif',
                fontSize: 42, fontWeight: 600, letterSpacing: -1.2,
                margin: '8px 0 12px', lineHeight: 1.02, color: '#0F0F0E'
              }}>{a.name}</h1>
              <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
                <Chip>Football</Chip>
                <Chip>NFL</Chip>
                <Chip tone="dark">Chrome</Chip>
                <span style={{ fontSize: 12, color: '#6B6757', marginLeft: 6 }}>
                  Featured in {window.INSERT_SETS.length + window.AUTOGRAPH_SETS.length} sets
                </span>
              </div>
            </div>

            {/* Team Details panel */}
            <TeamDetails td={window.TEAM_DETAILS} />
          </div>
        </div>

        {/* STAT STRIP — 4 athlete totals */}
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
          background: '#FFFFFF', borderBottom: '1px solid #EDEAE0'
        }}>
          {[
          ['CARD TYPES', a.cardTypes.toString()],
          ['TOTAL CARDS', a.totalCards.toLocaleString()],
          ['NUMBERED PARALLELS', a.numberedParallels.toLocaleString()],
          ['1/1S', a.oneOfOnes.toString()]].
          map(([label, val], i) =>
          <div key={label} style={{
            padding: '18px 22px',
            borderRight: i < 3 ? '1px solid #EDEAE0' : 'none'
          }}>
              <div style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600
            }}>{label}</div>
              <div style={{
              fontFamily: '"Inter Tight", Inter, sans-serif',
              fontSize: 26, fontWeight: 600, letterSpacing: -0.6, color: '#0F0F0E',
              marginTop: 4
            }}>{val}</div>
            </div>
          )}
        </div>

        {/* PRIMARY TABS */}
        <div style={{
          display: 'flex', gap: 0, padding: '0 36px',
          background: '#FAFAF7', borderBottom: '1px solid #EDEAE0'
        }}>
          {tabs.map((t) =>
          <button key={t} onClick={() => setTab(t)} style={{
            padding: '14px 20px', background: 'none', border: 'none',
            borderBottom: tab === t ? '2px solid #0F0F0E' : '2px solid transparent',
            marginBottom: -1, color: tab === t ? '#0F0F0E' : '#8A8677',
            fontFamily: 'inherit', fontSize: 13,
            fontWeight: tab === t ? 600 : 500, cursor: 'pointer'
          }}>{t}</button>
          )}
        </div>

        {/* CONTENT */}
        <main style={{ padding: '28px 36px 60px' }}>
          {tab === 'Overview' &&
          <>
              <BreakCalc calc={calc} cases={cases} boxes={boxes} setCases={setCases} setBoxes={setBoxes} />
              <SectionHead>Insert Sets</SectionHead>
              <AccordionList
              items={window.INSERT_SETS}
              openName={openSet}
              onToggle={(n) => setOpenSet(openSet === n ? null : n)} />
            
              <SectionHead>Autographs</SectionHead>
              <AutographsTable />
            </>
          }

          {tab === 'Card Types' &&
          <AccordionList
            items={window.INSERT_SETS}
            openName={openSet}
            onToggle={(n) => setOpenSet(openSet === n ? null : n)} />

          }

          {tab === 'Inserts' &&
          <InsertsTable />
          }

          {tab === 'Base Parallels' &&
          <ParallelsTable />
          }

          {tab === 'Autographs' &&
          <AutographsTable />
          }

          {tab === 'Also Featured In' &&
          <AlsoFeaturedInTable />
          }
        </main>
      </div>
    </div>);

}

// ─── Sub-components ────────────────────────────────────────────────────────

function SectionHead({ children }) {
  return (
    <div style={{
      fontFamily: '"Inter Tight", Inter, sans-serif',
      fontSize: 16, fontWeight: 600, letterSpacing: -0.3, color: '#0F0F0E',
      margin: '28px 0 12px'
    }}>{children}</div>);

}

function TeamDetails({ td }) {
  return (
    <div style={{
      background: '#FAFAF7',
      padding: '14px 16px', borderWidth: "2px 2px 2px 1px", borderStyle: "solid", borderColor: "rgb(237, 234, 224)", borderImage: "initial", borderRadius: "0px", border: "2px solid rgb(242, 240, 233)"
    }}>
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        marginBottom: 10
      }}>
        <div style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600
        }}>TEAM DETAILS</div>
        <a href="#" style={{
          fontSize: 10, color: '#3A372F', textDecoration: 'none',
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          letterSpacing: 0.6, fontWeight: 600
        }}>VIEW TEAM →</a>
      </div>
      <div style={{
        fontFamily: '"Inter Tight", Inter, sans-serif',
        fontSize: 15, fontWeight: 600, letterSpacing: -0.2, color: '#0F0F0E',
        marginBottom: 8
      }}>{td.team}</div>
      {[
      ['Athletes in set', td.athletesInSet],
      ['Total cards', td.totalCards.toLocaleString()],
      ['Autographs', td.autographs],
      ['Rookies', td.rookies],
      ['Numbered parallels', td.numberedParallels.toLocaleString()]].
      map(([k, v]) =>
      <div key={k} style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '4px 0', fontSize: 11, color: '#3A372F'
      }}>
          <span>{k}</span>
          <span style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontWeight: 600, color: '#0F0F0E'
        }}>{v}</span>
        </div>
      )}
    </div>);

}

function AthletePhoto({ name, team, src }) {
  // Square photo slot — bound to athlete image API in production.
  // If no src is provided, render a neutral placeholder with the athlete's
  // initials and a small "PHOTO" mono caption so it's clear what fills the box.
  const initials = name.split(' ').map((p) => p[0]).join('').slice(0, 2);
  return (
    <div style={{
      width: 180, height: 180, position: 'relative',
      background: '#F1EFE9', border: '1px solid #EDEAE0',
      overflow: 'hidden'
    }}>
      {src ?
      <img src={src} alt={name} style={{
        width: '100%', height: '100%', objectFit: 'cover', display: 'block'
      }} /> :

      <>
          <div style={{
          position: 'absolute', inset: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: '"Inter Tight", Inter, sans-serif',
          fontSize: 64, fontWeight: 600, letterSpacing: -2,
          color: '#C4BEAD'
        }}>{initials}</div>
          <div style={{
          position: 'absolute', top: 10, left: 10,
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600
        }}>PHOTO</div>
          <div style={{
          position: 'absolute', bottom: 10, left: 10, right: 10,
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 9, letterSpacing: 1.4, color: '#8A8677', fontWeight: 600,
          display: 'flex', justifyContent: 'space-between'
        }}>
            <span>{team.toUpperCase()}</span>
            <span>API</span>
          </div>
        </>
      }
    </div>);

}

function AthleteCard({ name, team, jersey, position }) {
  // Hero card art — autograph-style insert visual.
  // Two-panel: top photo placeholder (subtle stripe), bottom signature panel.
  return (
    <div style={{
      aspectRatio: '2/2.8', height: 172, width: 122,
      background: '#0F0F0E', position: 'relative', overflow: 'hidden',
      boxShadow: '0 12px 28px rgba(15,15,14,0.18)',
      transform: 'rotate(-3deg)',
      border: '4px solid #FFFFFF'
    }}>
      {/* Top half — photo placeholder w/ team color wash */}
      <div style={{
        position: 'absolute', top: 0, left: 0, right: 0, height: '60%',
        background: 'linear-gradient(160deg, #C2102E 0%, #6B0A1B 100%)'
      }}>
        {/* subtle grid pattern */}
        <div style={{
          position: 'absolute', inset: 0,
          backgroundImage: 'repeating-linear-gradient(45deg, rgba(255,255,255,0.06) 0 2px, transparent 2px 8px)'
        }} />
        <div style={{
          position: 'absolute', top: 8, left: 8,
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 8, fontWeight: 700, color: '#FFF', letterSpacing: 1.5
        }}>{team.toUpperCase()}</div>
        <div style={{
          position: 'absolute', top: 8, right: 8,
          fontFamily: '"Inter Tight", sans-serif',
          fontSize: 22, fontWeight: 700, color: 'rgba(255,255,255,0.9)', lineHeight: 1
        }}>{jersey}</div>
      </div>
      {/* Auto card middle band */}
      <div style={{
        position: 'absolute', top: '60%', left: 0, right: 0, height: '8%',
        background: 'linear-gradient(90deg, #E8C75A 0%, #F8E7A6 50%, #C9A537 100%)',
        display: 'flex', alignItems: 'center', justifyContent: 'center'
      }}>
        <span style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 6, fontWeight: 700, color: '#3A2A05', letterSpacing: 1.5
        }}>AUTOGRAPH CARD</span>
      </div>
      {/* Signature panel */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0, height: '32%',
        background: '#F4EFE3',
        padding: '6px 8px'
      }}>
        {/* fake signature stroke */}
        <svg viewBox="0 0 100 24" style={{ width: '100%', height: 18, display: 'block' }}>
          <path d="M2,16 C8,4 14,18 22,12 C30,6 36,18 44,14 C52,10 60,18 68,8 C74,2 84,16 96,10"
          stroke="#142A6E" strokeWidth="1.4" fill="none" strokeLinecap="round" />
        </svg>
        <div style={{
          fontFamily: '"Inter Tight", sans-serif',
          fontSize: 9, fontWeight: 700, color: '#0F0F0E', marginTop: 2
        }}>{name.toUpperCase()}</div>
        <div style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 6, color: '#6B6757', letterSpacing: 0.8, marginTop: 1
        }}>{position} · {team.toUpperCase()}</div>
      </div>
    </div>);

}

function BreakCalc({ calc, cases, boxes, setCases, setBoxes }) {
  return (
    <div style={{
      background: '#FFFFFF',
      padding: '20px 22px', borderStyle: "solid", borderColor: "rgb(237, 234, 224)", borderImage: "initial", borderWidth: "2px 2px 1px 1px", borderRadius: "0px", border: "2px solid rgb(21, 20, 18)"
    }}>
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start',
        marginBottom: 16, gap: 16
      }}>
        <div>
          <div style={{
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600
          }}>BREAK HIT CALCULATOR</div>
          <div style={{
            fontFamily: '"Inter Tight", Inter, sans-serif',
            fontSize: 18, fontWeight: 600, letterSpacing: -0.4, color: '#0F0F0E',
            marginTop: 4
          }}>How likely is Drake Maye in your break?</div>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <Stepper label="CASES" value={cases} onChange={setCases} />
          <Stepper label="BOXES" value={boxes} onChange={setBoxes} />
        </div>
      </div>
      {calc.rows.map((r) => {
        const dot = r.tone === 'good' ? '#0E8A4F' : r.tone === 'medium' ? '#C28A18' : '#9A2B14';
        const oddsColor = dot;
        return (
          <div key={r.label} style={{
            display: 'grid', gridTemplateColumns: '20px 1fr 110px 160px',
            alignItems: 'center', gap: 12,
            padding: '12px 0', borderTop: '1px solid #F4F1E8'
          }}>
            <span style={{
              width: 8, height: 8, borderRadius: '50%', background: dot,
              justifySelf: 'center'
            }} />
            <div>
              <div style={{ fontSize: 14, fontWeight: 600, color: '#0F0F0E' }}>{r.label}</div>
              <div style={{ fontSize: 12, color: '#6B6757', marginTop: 2 }}>{r.sub}</div>
            </div>
            <div style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 16, fontWeight: 600, color: oddsColor, textAlign: 'right'
            }}>{r.odds}</div>
            <div style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 12, color: '#6B6757', textAlign: 'right'
            }}>{r.perBox}</div>
          </div>);

      })}
      <div style={{
        marginTop: 14, padding: '10px 12px', background: '#FAFAF7', borderRadius: 6,
        fontSize: 11, color: '#8A8677',
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace', letterSpacing: 0.4
      }}>
        ALL PROBABILITIES BASED ON OFFICIAL PACK ODDS · {cases} CASE{cases !== 1 ? 'S' : ''} · {boxes} BOX{boxes !== 1 ? 'ES' : ''} · {boxes * 20} PACKS
      </div>
    </div>);

}

function Stepper({ label, value, onChange }) {
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
        marginBottom: 4, textAlign: 'right'
      }}>{label}</div>
      <div style={{
        display: 'flex', alignItems: 'center', gap: 0,
        border: '1px solid #EDEAE0', borderRadius: 6, overflow: 'hidden'
      }}>
        <button onClick={() => onChange(Math.max(1, value - 1))} style={stepBtn}>−</button>
        <div style={{
          minWidth: 36, textAlign: 'center', padding: '6px 10px', fontSize: 13, fontWeight: 600,
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          borderLeft: '1px solid #EDEAE0', borderRight: '1px solid #EDEAE0', background: '#FFF'
        }}>{value}</div>
        <button onClick={() => onChange(value + 1)} style={stepBtn}>+</button>
      </div>
    </div>);

}
const stepBtn = {
  padding: '6px 10px', background: '#FFF', border: 'none', cursor: 'pointer',
  fontSize: 14, color: '#3A372F', fontFamily: 'inherit'
};

function AccordionList({ items, openName, onToggle }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
      {items.map((s) => {
        const open = s.name === openName;
        return (
          <div key={s.name} style={{
            border: open ? '1.5px solid #0F0F0E' : '1px solid #EDEAE0',
            borderRadius: 8, background: '#FFFFFF', overflow: 'hidden'
          }}>
            <button onClick={() => onToggle(s.name)} style={{
              width: '100%', padding: '14px 18px', display: 'flex',
              justifyContent: 'space-between', alignItems: 'center',
              background: 'transparent', border: 'none', cursor: 'pointer',
              fontFamily: 'inherit', textAlign: 'left'
            }}>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
                <span style={{ fontSize: 14, fontWeight: 600, color: '#0F0F0E' }}>{s.name}</span>
                <span style={{
                  fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize: 11, color: '#8A8677'
                }}>{s.cards} card{s.cards !== 1 ? 's' : ''} · {s.parallels} parallel{s.parallels !== 1 ? 's' : ''}</span>
              </div>
              <IconChev dir={open ? 'up' : 'down'} size={14} color="#3A372F" />
            </button>
            {open && s.details && <AccordionDetail d={s.details} isAuto={s.isAutograph} />}
            {open && !s.details && <AccordionEmpty />}
          </div>);

      })}
    </div>);

}

function AccordionDetail({ d, isAuto }) {
  if (isAuto) return <AutographDetail d={d} />;
  const toneMap = {
    silver: { bg: '#E6E3D9', fg: '#3A372F' },
    orange: { bg: '#F1D4B8', fg: '#7A3F0E' },
    teal: { bg: '#BFE0DA', fg: '#15554C' },
    blue: { bg: '#C8D3E8', fg: '#1F3A6A' },
    green: { bg: '#C7DFC4', fg: '#1F4F22' },
    black: { bg: '#3A372F', fg: '#FAFAF7' },
    red: { bg: '#E8C2BD', fg: '#7A1A12' },
    gold: { bg: '#F0D88A', fg: '#5A3F0A' }
  };
  return (
    <div style={{ padding: '0 18px 18px' }}>
      <div style={{
        display: 'flex', gap: 14, alignItems: 'center',
        padding: '10px 0 14px', borderTop: '1px solid #F4F1E8'
      }}>
        <span style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 11, fontWeight: 600, color: '#0F0F0E',
          background: '#F1EFE9', padding: '3px 7px', borderRadius: 3
        }}>{d.cardNumber}</span>
        <span style={{ fontSize: 13, fontWeight: 600, color: '#0F0F0E' }}>{d.subject}</span>
        <span style={{ fontSize: 12, color: '#6B6757' }}>{d.team}</span>
      </div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
        marginBottom: 8
      }}>PARALLELS</div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
        {d.parallels.map((p) => {
          const t = toneMap[p.tone] || toneMap.silver;
          return (
            <span key={p.name} style={{
              display: 'inline-flex', alignItems: 'baseline', gap: 6,
              padding: '5px 10px', borderRadius: 4, fontSize: 11, fontWeight: 500,
              background: t.bg, color: t.fg
            }}>
              <span>{p.name}</span>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 10, opacity: 0.75
              }}>{p.run}</span>
            </span>);

        })}
      </div>
    </div>);

}

function AccordionEmpty() {
  return (
    <div style={{
      padding: '0 18px 14px'
    }}>
      <div style={{
        padding: '10px 0', borderTop: '1px solid #F4F1E8',
        fontSize: 12, color: '#8A8677', fontStyle: 'italic'
      }}>Expand for card numbers and parallel print runs.</div>
    </div>);

}

function ParallelsTable() {
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#6B6757', fontWeight: 600,
        padding: '0 10px 8px', borderBottom: '1px solid #EDEAE0',
        display: 'grid', gridTemplateColumns: '1fr 90px 100px 160px'
      }}>
        <span>BASE PARALLELS</span>
        <span style={{ textAlign: 'right' }}>PRINT RUN</span>
        <span style={{ textAlign: 'right' }}>PACK ODDS</span>
        <span style={{ textAlign: 'right' }}>PER BOX (20 PACKS)</span>
      </div>
      {window.BASE_PARALLELS.map((p) =>
      <div key={p.name} style={{
        display: 'grid', gridTemplateColumns: '1fr 90px 100px 160px',
        padding: '11px 10px', borderBottom: '1px solid #F4F1E8',
        fontSize: 13, color: p.rare ? '#9A2B14' : '#0F0F0E'
      }}>
          <span>{p.name}</span>
          <span style={{
          textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          color: p.run === 'unnumbered' ? '#B7B2A3' : p.rare ? '#9A2B14' : '#0F0F0E',
          fontWeight: p.run === 'unnumbered' ? 400 : 600
        }}>{p.run === 'unnumbered' ? '—' : p.run}</span>
          <span style={{ textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace' }}>{p.odds}</span>
          <span style={{ textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace', color: '#6B6757' }}>{p.per}</span>
        </div>
      )}
    </div>);

}

function AutographDetail({ d }) {
  return (
    <div style={{ padding: '0 18px 18px' }}>
      <div style={{
        display: 'flex', gap: 14, alignItems: 'center',
        padding: '10px 0 14px', borderTop: '1px solid #F4F1E8'
      }}>
        <span style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 11, fontWeight: 600, color: '#0F0F0E',
          background: '#F1EFE9', padding: '3px 7px', borderRadius: 3
        }}>{d.cardNumber}</span>
        <span style={{ fontSize: 13, fontWeight: 600, color: '#0F0F0E' }}>{d.subject}</span>
        <span style={{ fontSize: 12, color: '#6B6757' }}>{d.team}</span>
      </div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#6B6757', fontWeight: 600,
        padding: '0 0 8px', borderBottom: '1px solid #EDEAE0',
        display: 'grid', gridTemplateColumns: '1fr 90px 100px 160px'
      }}>
        <span>AUTOGRAPH PARALLELS</span>
        <span style={{ textAlign: 'right' }}>PRINT RUN</span>
        <span style={{ textAlign: 'right' }}>PACK ODDS</span>
        <span style={{ textAlign: 'right' }}>PER BOX (20 PACKS)</span>
      </div>
      {d.parallels.map((p) =>
      <div key={p.name} style={{
        display: 'grid', gridTemplateColumns: '1fr 90px 100px 160px',
        padding: '11px 0', borderBottom: '1px solid #F4F1E8',
        fontSize: 13, color: p.rare ? '#9A2B14' : '#0F0F0E'
      }}>
          <span>{p.name}</span>
          <span style={{
          textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          color: p.rare ? '#9A2B14' : '#0F0F0E', fontWeight: 600
        }}>{p.run}</span>
          <span style={{ textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace' }}>{p.odds || '—'}</span>
          <span style={{ textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace', color: '#6B6757' }}>{p.per || '—'}</span>
        </div>
      )}
    </div>);

}

function AutographsTable() {
  const cols = '1fr 90px 100px 160px';
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#6B6757', fontWeight: 600,
        padding: '0 10px 8px', borderBottom: '1px solid #EDEAE0',
        display: 'grid', gridTemplateColumns: cols
      }}>
        <span>AUTOGRAPH PARALLELS</span>
        <span style={{ textAlign: 'right' }}>PRINT RUN</span>
        <span style={{ textAlign: 'right' }}>PACK ODDS</span>
        <span style={{ textAlign: 'right' }}>PER BOX (20 PACKS)</span>
      </div>
      {window.AUTOGRAPH_SETS.map((s, si) =>
      <React.Fragment key={s.name}>
          <div style={{
          display: 'grid', gridTemplateColumns: '1fr auto',
          alignItems: 'baseline', gap: 12,
          padding: si === 0 ? '14px 10px 10px' : '22px 10px 10px',
          borderBottom: '1px solid #EDEAE0'
        }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, flexWrap: 'wrap' }}>
              <span style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 11, fontWeight: 600, color: '#0F0F0E',
              background: '#F1EFE9', padding: '3px 7px', borderRadius: 3
            }}>{s.cardNumber}</span>
              <span style={{ fontSize: 14, fontWeight: 600, color: '#0F0F0E', letterSpacing: -0.1 }}>{s.name}</span>
              <span style={{ fontSize: 12, color: '#6B6757' }}>{s.subject}</span>
              <span style={{ fontSize: 12, color: '#8A8677' }}>· {s.team}</span>
            </div>
            <span style={{
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize: 10, letterSpacing: 1.2, color: '#8A8677', fontWeight: 600
          }}>{s.parallels.length} PARALLELS</span>
          </div>
          {s.parallels.map((p) =>
        <div key={s.name + p.name} style={{
          display: 'grid', gridTemplateColumns: cols,
          padding: '11px 10px', borderBottom: '1px solid #F4F1E8',
          fontSize: 13, color: p.rare ? '#9A2B14' : '#0F0F0E'
        }}>
              <span>{p.name}</span>
              <span style={{
            textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontWeight: 600, color: p.rare ? '#9A2B14' : '#0F0F0E'
          }}>{p.run}</span>
              <span style={{ textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace' }}>{p.odds}</span>
              <span style={{ textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace', color: p.rare ? '#9A2B14' : '#6B6757' }}>{p.per}</span>
            </div>
        )}
        </React.Fragment>
      )}
    </div>);

}

function InsertsTable() {
  const cols = '1fr 100px 110px';
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#6B6757', fontWeight: 600,
        padding: '0 10px 8px', borderBottom: '1px solid #EDEAE0',
        display: 'grid', gridTemplateColumns: cols
      }}>
        <span>INSERT PARALLELS</span>
        <span style={{ textAlign: 'right' }}>PRINT RUN</span>
        <span style={{ textAlign: 'right' }}>PACK ODDS</span>
      </div>
      {window.INSERT_TABLE.map((s, si) =>
        <React.Fragment key={s.name}>
          <div style={{
            display: 'grid', gridTemplateColumns: '1fr auto',
            alignItems: 'baseline', gap: 12,
            padding: si === 0 ? '14px 10px 10px' : '22px 10px 10px',
            borderBottom: '1px solid #EDEAE0'
          }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, flexWrap: 'wrap' }}>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 11, fontWeight: 600, color: '#0F0F0E',
                background: '#F1EFE9', padding: '3px 7px', borderRadius: 3
              }}>{s.cardNumber}</span>
              <span style={{ fontSize: 14, fontWeight: 600, color: '#0F0F0E', letterSpacing: -0.1 }}>{s.name}</span>
              <span style={{ fontSize: 12, color: '#6B6757' }}>{s.subject}</span>
            </div>
            <span style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 10, letterSpacing: 1.2, color: '#8A8677', fontWeight: 600
            }}>{s.parallels.length} PARALLELS</span>
          </div>
          {s.parallels.map((p) =>
            <div key={s.name + p.name} style={{
              display: 'grid', gridTemplateColumns: cols,
              padding: '11px 10px', borderBottom: '1px solid #F4F1E8',
              fontSize: 13, color: p.rare ? '#9A2B14' : '#0F0F0E'
            }}>
              <span>{p.name}</span>
              <span style={{
                textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontWeight: p.run === 'unnumbered' ? 400 : 600,
                color: p.run === 'unnumbered' ? '#B7B2A3' : (p.rare ? '#9A2B14' : '#0F0F0E')
              }}>{p.run === 'unnumbered' ? '—' : p.run}</span>
              <span style={{
                textAlign: 'right', fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                color: p.rare ? '#9A2B14' : '#0F0F0E'
              }}>{p.odds}</span>
            </div>
          )}
        </React.Fragment>
      )}
    </div>
  );
}

function AlsoFeaturedInTable() {
  const cols = '1.6fr 1fr 70px 80px 70px 90px';
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#6B6757', fontWeight: 600,
        padding: '0 10px 8px', borderBottom: '1px solid #EDEAE0',
        display: 'grid', gridTemplateColumns: cols, gap: 12
      }}>
        <span>SET</span>
        <span>BRAND</span>
        <span style={{ textAlign: 'right' }}>YEAR</span>
        <span style={{ textAlign: 'right' }}>HIS CARDS</span>
        <span style={{ textAlign: 'right' }}>AUTOS</span>
        <span style={{ textAlign: 'right' }}>PARALLELS</span>
      </div>
      {window.ALSO_APPEARS_IN.map(s =>
        <div key={s.name} style={{
          display: 'grid', gridTemplateColumns: cols, gap: 12,
          padding: '14px 10px', borderBottom: '1px solid #F4F1E8',
          fontSize: 13, color: '#0F0F0E', alignItems: 'baseline'
        }}>
          <a href="#" style={{
            color: '#0F0F0E', textDecoration: 'none', fontWeight: 600,
          }}>{s.name}</a>
          <span style={{ color: '#3A372F' }}>{s.brand}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            color: '#3A372F'
          }}>{s.year}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontWeight: 600
          }}>{s.cards}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            color: s.autos === 0 ? '#B7B2A3' : '#3A372F',
          }}>{s.autos === 0 ? '—' : s.autos}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            color: '#3A372F'
          }}>{s.parallels}</span>
        </div>
      )}
    </div>
  );
}

window.AthleteDetailD = AthleteDetailD;