// Team Detail (Mobile / iOS) — companion to TeamDetailD.
// Same content adapted to a narrow viewport:
//   - Sticky compact app bar with hamburger that opens the Teams drawer
//   - Hero: square crest + identity + chips
//   - Roster summary card
//   - 4 stat tiles in a row
//   - Sticky horizontal-scroll tabs
//   - Athletes tab: card-style list (avatar + name + 4-up stat strip)

function TeamDetailDMobile({ initialDrawerOpen = false } = {}) {
  const t = window.TEAM_DETAIL;
  const athletes = window.TEAM_ATHLETES;
  const teams = window.TEAMS_IN_SET;
  const [tab, setTab] = React.useState('Athletes');
  const [drawerOpen, setDrawerOpen] = React.useState(initialDrawerOpen);
  const [sort, setSort] = React.useState({ key: 'totalCards', dir: 'desc' });
  const [position, setPosition] = React.useState('All Positions');
  const [rookiesOnly, setRookiesOnly] = React.useState(false);
  const tabs = ['Overview', 'Athletes', 'Inserts', 'Autographs', 'Numbered Parallels'];
  const positions = React.useMemo(() => {
    const set = new Set(athletes.map((a) => a.position));
    return ['All Positions', ...Array.from(set).sort()];
  }, [athletes]);
  const sortKeys = [
    { key: 'totalCards',        label: 'Total Cards' },
    { key: 'autographs',        label: 'Autographs' },
    { key: 'inserts',           label: 'Inserts' },
    { key: 'numberedParallels', label: 'Numbered' },
  ];

  const sorted = React.useMemo(() => {
    const arr = [...athletes];
    arr.sort((a, b) => {
      const av = a[sort.key];
      const bv = b[sort.key];
      if (typeof av === 'string') {
        return sort.dir === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
      }
      return sort.dir === 'asc' ? av - bv : bv - av;
    });
    return arr.filter((a) => {
      if (position !== 'All Positions' && a.position !== position) return false;
      if (rookiesOnly && !a.rookie) return false;
      return true;
    });
  }, [athletes, sort, position, rookiesOnly]);

  return (
    <div style={{
      width: '100%', minHeight: '100%', background: '#FAFAF7',
      color: '#0F0F0E', fontFamily: 'Inter, system-ui, sans-serif',
      paddingTop: 54,
      position: 'relative',
    }}>
      {/* APP TOP BAR */}
      <div style={{
        position: 'sticky', top: 54, zIndex: 10,
        background: 'rgba(250,250,247,0.92)',
        backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',
        borderBottom: '1px solid #EDEAE0',
        padding: '10px 14px', display: 'flex', alignItems: 'center', gap: 10,
      }}>
        <button onClick={() => setDrawerOpen(true)} aria-label="Teams" style={{
          background: '#FFFFFF', border: '1px solid #E6E3D9', borderRadius: 8,
          padding: '8px 10px', display: 'flex', alignItems: 'center', gap: 6,
          fontSize: 12, fontWeight: 500, color: '#3A372F', cursor: 'pointer',
          fontFamily: 'inherit',
        }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <rect x="3.5" y="4.5" width="7" height="7" rx="1" stroke="#3A372F" strokeWidth="1.6"/>
            <rect x="13.5" y="4.5" width="7" height="7" rx="1" stroke="#3A372F" strokeWidth="1.6"/>
            <rect x="3.5" y="13.5" width="7" height="7" rx="1" stroke="#3A372F" strokeWidth="1.6"/>
            <rect x="13.5" y="13.5" width="7" height="7" rx="1" stroke="#3A372F" strokeWidth="1.6"/>
          </svg>
          Teams
        </button>
        <a href={t.setHref} style={{
          flex: 1, minWidth: 0,
          fontSize: 11, color: '#6B6757', textDecoration: 'none',
          display: 'inline-flex', alignItems: 'center', gap: 4,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>
          <IconChev dir="left" size={11} color="#6B6757"/>
          <span style={{
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          }}>{t.setName}</span>
        </a>
      </div>

      {/* HERO */}
      <div style={{
        padding: '16px 14px 14px', background: '#FFFFFF',
        borderBottom: '1px solid #EDEAE0',
      }}>
        <div style={{ display: 'flex', gap: 14, alignItems: 'flex-start' }}>
          <TeamCrest name={t.teamShort} primary={t.primary} secondary={t.secondary} size={96}/>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
            }}>{t.league} · {t.conference}</div>
            <h1 style={{
              fontFamily: '"Inter Tight", Inter, sans-serif',
              fontSize: 22, fontWeight: 600, letterSpacing: -0.6,
              margin: '4px 0 8px', lineHeight: 1.05, color: '#0F0F0E',
            }}>{t.team}</h1>
            <div style={{ display: 'flex', gap: 5, alignItems: 'center', flexWrap: 'wrap' }}>
              <Chip>{t.league}</Chip>
              <Chip tone="dark">Chrome</Chip>
            </div>
          </div>
        </div>
      </div>

      {/* STAT GRID */}
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
        background: '#FFFFFF', borderBottom: '1px solid #EDEAE0',
      }}>
        {[
          ['ATHLETES', t.athletes.toString()],
          ['CARDS', t.totalCards.toLocaleString()],
          ['NUMBERED', t.numberedParallels.toLocaleString()],
          ['1/1S', t.oneOfOnes.toString()],
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

      {/* TABS */}
      <div style={{
        position: 'sticky', top: 54 + 41, zIndex: 9,
        display: 'flex', gap: 0, padding: '0 14px',
        background: '#FAFAF7', borderBottom: '1px solid #EDEAE0',
        overflowX: 'auto', WebkitOverflowScrolling: 'touch',
      }}>
        {tabs.map((tb) => (
          <button key={tb} onClick={() => setTab(tb)} style={{
            padding: '12px 12px', background: 'none', border: 'none',
            borderBottom: tab === tb ? '2px solid #0F0F0E' : '2px solid transparent',
            marginBottom: -1, color: tab === tb ? '#0F0F0E' : '#8A8677',
            fontFamily: 'inherit', fontSize: 13, whiteSpace: 'nowrap',
            fontWeight: tab === tb ? 600 : 500, cursor: 'pointer',
          }}>{tb}</button>
        ))}
      </div>

      {/* CONTENT */}
      <main style={{ padding: '14px' }}>
        {(tab === 'Overview' || tab === 'Athletes') && (
          <>
            {tab === 'Overview' && (
              <>
                <RosterSummaryMobile t={t}/>
                <div style={{
                  fontFamily: '"Inter Tight", Inter, sans-serif',
                  fontSize: 16, fontWeight: 600, letterSpacing: -0.3, color: '#0F0F0E',
                  margin: '14px 0 10px',
                }}>Athletes</div>
              </>
            )}
            {/* Filter row */}
            <div style={{
              display: 'flex', gap: 8, marginBottom: 10, alignItems: 'center',
              flexWrap: 'wrap',
            }}>
              <div style={{ flex: 1, minWidth: 140 }}>
                <SelectMobile value={position} onChange={setPosition} options={positions}/>
              </div>
              <label style={{
                display: 'inline-flex', alignItems: 'center', gap: 6,
                fontSize: 12, color: '#3A372F', cursor: 'pointer',
              }}>
                <input type="checkbox" checked={rookiesOnly}
                  onChange={(e) => setRookiesOnly(e.target.checked)}
                  style={{ accentColor: '#0F0F0E' }}/>
                Rookies
              </label>
            </div>
            {/* Sort chips */}
            <div style={{ display: 'flex', gap: 6, marginBottom: 12, flexWrap: 'wrap' }}>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 9, letterSpacing: 1.4, color: '#8A8677', fontWeight: 600,
                alignSelf: 'center', marginRight: 2,
              }}>SORT</span>
              {sortKeys.map((s) => {
                const active = sort.key === s.key;
                return (
                  <button key={s.key} onClick={() => setSort({
                    key: s.key, dir: active && sort.dir === 'desc' ? 'asc' : 'desc',
                  })} style={{
                    padding: '4px 10px', borderRadius: 999, fontSize: 11, fontWeight: 500,
                    fontFamily: 'inherit', cursor: 'pointer',
                    background: active ? '#0F0F0E' : '#FFFFFF',
                    color: active ? '#FAFAF7' : '#3A372F',
                    border: active ? '1px solid #0F0F0E' : '1px solid #E6E3D9',
                    display: 'inline-flex', alignItems: 'center', gap: 4,
                  }}>
                    {s.label}
                    {active && <span style={{ fontSize: 8 }}>{sort.dir === 'asc' ? '▲' : '▼'}</span>}
                  </button>
                );
              })}
            </div>
            <AthletesListMobile rows={sorted}/>
          </>
        )}

        {tab === 'Inserts' && <PlaceholderMobile label="Insert breakdown by athlete — coming soon"/>}
        {tab === 'Autographs' && <PlaceholderMobile label="Autograph breakdown by athlete — coming soon"/>}
        {tab === 'Numbered Parallels' && <PlaceholderMobile label="Numbered parallel breakdown by athlete — coming soon"/>}

        <div style={{ height: 40 }}/>
      </main>

      {/* DRAWER */}
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
            }}>Teams in Set</div>
            <span style={{ flex: 1 }}/>
            <span style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 11, color: '#8A8677',
            }}>{teams.length}</span>
          </div>
          <div style={{ flex: 1, overflowY: 'auto', padding: '14px 16px 30px' }}>
            <div style={{
              background: '#F1EFE9', borderRadius: 10, padding: '9px 12px',
              display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14,
            }}>
              <IconSearch size={15}/>
              <input placeholder="Search teams…" style={{
                flex: 1, border: 'none', background: 'transparent', outline: 'none',
                fontSize: 14, fontFamily: 'inherit', color: '#0F0F0E',
              }}/>
            </div>
            <div style={{
              display: 'flex', justifyContent: 'space-between',
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
              padding: '8px 4px', borderBottom: '1px solid #EDEAE0',
            }}>
              <span>TEAM</span><span>ATHLETES</span>
            </div>
            {teams.map((tm) => {
              const selected = tm.name === t.team;
              return (
                <div key={tm.name} style={{
                  display: 'flex', alignItems: 'center', gap: 12,
                  padding: '12px 8px', borderBottom: '1px solid #F4F1E8',
                  background: selected ? '#F4F1E8' : 'transparent',
                  borderLeft: selected ? '2px solid #0F0F0E' : '2px solid transparent',
                  marginLeft: selected ? -8 : 0, paddingLeft: selected ? 14 : 4,
                }}>
                  <TeamCrest name={tm.short}
                    primary={selected ? t.primary : '#3A372F'}
                    secondary={selected ? t.secondary : '#8A8677'} size={36}/>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 14, fontWeight: 600 }}>{tm.short}</div>
                    <div style={{ fontSize: 12, color: '#6B6757', marginTop: 1 }}>{tm.totalCards.toLocaleString()} cards</div>
                  </div>
                  <span style={{
                    fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                    fontSize: 14, fontWeight: 600, color: '#0F0F0E',
                  }}>{tm.athletes}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

function TeamDetailDMobileOpen() {
  return <TeamDetailDMobile initialDrawerOpen={true}/>;
}

// ─── Mobile sub-components ─────────────────────────────────────────────────

function RosterSummaryMobile({ t }) {
  return (
    <div style={{
      background: '#FFFFFF', border: '1px solid #EDEAE0', borderRadius: 10,
      padding: '14px 14px',
    }}>
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        marginBottom: 8,
      }}>
        <div style={{
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
        }}>ROSTER SUMMARY</div>
        <a href="#" style={{
          fontSize: 10, color: '#3A372F', textDecoration: 'none',
          fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
          letterSpacing: 0.6, fontWeight: 600,
        }}>VIEW TEAM →</a>
      </div>
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', rowGap: 4, columnGap: 16,
      }}>
        {[
          ['Athletes in set', t.athletes],
          ['Total cards', t.totalCards.toLocaleString()],
          ['Autographs', t.autographs],
          ['Rookies', t.rookies],
          ['Numbered parallels', t.numberedParallels.toLocaleString()],
          ['1/1s', t.oneOfOnes],
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

function SelectMobile({ value, onChange, options }) {
  return (
    <div style={{
      position: 'relative',
      border: '1px solid #E6E3D9', borderRadius: 8, background: '#FFFFFF',
    }}>
      <select value={value} onChange={(e) => onChange(e.target.value)} style={{
        width: '100%', appearance: 'none', WebkitAppearance: 'none',
        background: 'transparent', border: 'none', outline: 'none',
        padding: '9px 30px 9px 12px', fontSize: 13, fontFamily: 'inherit',
        color: '#0F0F0E', cursor: 'pointer',
      }}>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
      <span style={{
        position: 'absolute', right: 12, top: '50%',
        transform: 'translateY(-50%)', pointerEvents: 'none',
        display: 'inline-flex',
      }}>
        <IconChev dir="down" size={11} color="#6B6757"/>
      </span>
    </div>
  );
}

function AthletesListMobile({ rows }) {
  return (
    <div style={{
      background: '#FFFFFF', border: '1px solid #EDEAE0', borderRadius: 10,
      overflow: 'hidden',
    }}>
      {rows.map((a, i) => (
        <a key={a.rank} href="#" style={{
          display: 'block', padding: '12px 14px',
          borderBottom: i < rows.length - 1 ? '1px solid #F4F1E8' : 'none',
          textDecoration: 'none', color: '#0F0F0E',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
            <span style={{
              fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize: 11, color: '#8A8677', width: 18,
            }}>{a.rank}</span>
            <div style={{
              width: 32, height: 32, borderRadius: '50%', background: '#EAE6D9',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 11, fontWeight: 600, color: '#6B6757', flex: '0 0 auto',
            }}>{a.name.split(' ').map((p) => p[0]).join('').slice(0, 2)}</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                <span style={{ fontSize: 14, fontWeight: 600 }}>{a.name}</span>
                {a.rookie && <span style={{
                  fontSize: 9, fontWeight: 700, padding: '1px 4px', borderRadius: 2,
                  background: 'oklch(0.55 0.17 25)', color: '#FFF8F1', letterSpacing: 0.6,
                }}>RC</span>}
              </div>
              <div style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 10, letterSpacing: 1.2, color: '#8A8677', fontWeight: 600,
                marginTop: 2,
              }}>{a.position} · #{a.jersey}</div>
            </div>
          </div>
          {/* 4-up stat strip */}
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
            background: '#FAFAF7', borderRadius: 8,
            border: '1px solid #EDEAE0',
          }}>
            {[
              ['CARDS', a.totalCards.toLocaleString()],
              ['AUTOS', a.autographs === 0 ? '—' : a.autographs.toString()],
              ['INSERTS', a.inserts.toString()],
              ['NUMBERED', a.numberedParallels.toLocaleString()],
            ].map(([label, val], j) => (
              <div key={label} style={{
                padding: '8px 6px',
                borderRight: j < 3 ? '1px solid #EDEAE0' : 'none',
                textAlign: 'center', minWidth: 0,
              }}>
                <div style={{
                  fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize: 8, letterSpacing: 1.2, color: '#8A8677', fontWeight: 600,
                  whiteSpace: 'nowrap',
                }}>{label}</div>
                <div style={{
                  fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize: 13, fontWeight: 600, color: val === '—' ? '#B7B2A3' : '#0F0F0E',
                  marginTop: 2, whiteSpace: 'nowrap',
                }}>{val}</div>
              </div>
            ))}
          </div>
        </a>
      ))}
    </div>
  );
}

function PlaceholderMobile({ label }) {
  return (
    <div style={{
      background: '#FFFFFF', border: '1px dashed #E6E3D9', borderRadius: 10,
      padding: '32px 16px', textAlign: 'center',
      fontSize: 13, color: '#8A8677',
    }}>{label}</div>
  );
}

window.TeamDetailDMobile = TeamDetailDMobile;
window.TeamDetailDMobileOpen = TeamDetailDMobileOpen;
