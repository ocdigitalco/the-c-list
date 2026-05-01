// Team Detail (Desktop) — uses the same Option-D visual language as
// AthleteDetailD: 300px left rail (teams in set), right column with hero,
// stat strip, primary tabs, and a flat athletes table.

function TeamDetailD() {
  const t = window.TEAM_DETAIL;
  const athletes = window.TEAM_ATHLETES;
  const teams = window.TEAMS_IN_SET;
  const [tab, setTab] = React.useState('Athletes');
  const [sort, setSort] = React.useState({ key: 'totalCards', dir: 'desc' });
  const [position, setPosition] = React.useState('All Positions');
  const [rookiesOnly, setRookiesOnly] = React.useState(false);
  const tabs = ['Overview', 'Athletes', 'Inserts', 'Autographs', 'Numbered Parallels'];
  const positions = React.useMemo(() => {
    const set = new Set(athletes.map((a) => a.position));
    return ['All Positions', ...Array.from(set).sort()];
  }, [athletes]);

  const sorted = React.useMemo(() => {
    const arr = [...athletes];
    if (rookiesOnly) {/* filter applied below */}
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
      width: 1280, background: '#FAFAF7', color: '#0F0F0E',
      fontFamily: 'Inter, system-ui, sans-serif',
      display: 'grid', gridTemplateColumns: '300px 1fr', alignItems: 'stretch',
      borderTop: '1px solid #EDEAE0',
    }}>
      {/* LEFT — Athletes rail (athletes on this team in this set) */}
      <aside style={{
        borderRight: '1px solid #EDEAE0', background: '#FFFFFF',
        padding: '22px 18px',
      }}>
        <div style={{
          fontFamily: '"Inter Tight", Inter, sans-serif',
          fontSize: 15, fontWeight: 600, letterSpacing: -0.2, marginBottom: 12,
        }}>Athletes in Set</div>
        <div style={{
          background: '#F1EFE9', borderRadius: 8, padding: '7px 10px',
          display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10,
        }}>
          <IconSearch size={14}/>
          <input placeholder="Search athletes…" style={{
            flex: 1, border: 'none', background: 'transparent', outline: 'none',
            fontSize: 13, fontFamily: 'inherit', color: '#0F0F0E',
          }}/>
        </div>
        <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginBottom: 10 }}>
          {['Total Cards', 'Autos', 'Inserts', 'Numbered'].map((f, i) => {
            const active = i === 0;
            return (
              <button key={f} style={{
                padding: '4px 9px', borderRadius: 4, fontSize: 11, fontWeight: 500,
                fontFamily: 'inherit', cursor: 'pointer',
                background: active ? '#0F0F0E' : 'transparent',
                color: active ? '#FAFAF7' : '#3A372F',
                border: active ? '1px solid #0F0F0E' : '1px solid #E6E3D9',
              }}>{f}</button>
            );
          })}
        </div>
        <label style={{
          display: 'inline-flex', alignItems: 'center', gap: 6,
          fontSize: 11, color: '#3A372F', marginBottom: 14,
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
        {athletes.map((a, i) => {
          const selected = i === 0;
          return (
            <div key={a.rank} style={{
              display: 'flex', alignItems: 'center', gap: 10,
              padding: '10px 8px', borderBottom: '1px solid #F4F1E8',
              background: selected ? '#F4F1E8' : 'transparent',
              borderLeft: selected ? '2px solid #0F0F0E' : '2px solid transparent',
              marginLeft: selected ? -8 : 0, paddingLeft: selected ? 12 : 4,
              cursor: 'pointer',
            }}>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 11, color: '#8A8677', width: 18,
              }}>{a.rank}</span>
              <div style={{
                width: 30, height: 30, borderRadius: '50%',
                background: selected ? '#0F0F0E' : '#EAE6D9',
                flex: '0 0 auto', display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 10, fontWeight: 600,
                color: selected ? '#FAFAF7' : '#6B6757',
              }}>{a.name.split(' ').map((p) => p[0]).join('').slice(0, 2)}</div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                  <span style={{ fontSize: 13, fontWeight: 600, color: '#0F0F0E' }}>{a.name}</span>
                  {a.rookie && <span style={{
                    fontSize: 8, fontWeight: 700, padding: '1px 4px', borderRadius: 2,
                    background: 'oklch(0.55 0.17 25)', color: '#FFF8F1', letterSpacing: 0.6,
                  }}>RC</span>}
                </div>
                <div style={{ fontSize: 11, color: '#6B6757', marginTop: 1 }}>{a.position} · #{a.jersey}</div>
              </div>
              <span style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 13, fontWeight: 600, color: '#0F0F0E',
              }}>{a.totalCards}</span>
            </div>
          );
        })}
      </aside>

      {/* RIGHT — hero, stats, tabs, content */}
      <div>
        {/* HERO */}
        <div style={{
          background: '#FFFFFF', borderBottom: '1px solid #EDEAE0',
          padding: '22px 36px 28px',
        }}>
          {/* Breadcrumb */}
          <a href={t.setHref} style={{
            display: 'inline-flex', alignItems: 'center', gap: 6,
            fontSize: 12, color: '#6B6757', textDecoration: 'none', marginBottom: 18,
          }}>
            <IconChev dir="left" size={12} color="#6B6757"/>
            <span>{t.setName}</span>
          </a>

          <div style={{
            display: 'grid', gridTemplateColumns: '180px 1fr 280px',
            gap: 32, alignItems: 'center',
          }}>
            <TeamCrest name={t.teamShort} primary={t.primary} secondary={t.secondary} size={180}/>

            <div>
              <div style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 10, letterSpacing: 2.4, color: '#8A8677', fontWeight: 600,
              }}>{t.league} · {t.conference} · {t.city.toUpperCase()}</div>
              <h1 style={{
                fontFamily: '"Inter Tight", Inter, sans-serif',
                fontSize: 38, fontWeight: 600, letterSpacing: -1.0,
                margin: '8px 0 14px', lineHeight: 1.08, color: '#0F0F0E',
                textWrap: 'balance',
              }}>{t.team}</h1>
              <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
                <Chip>{t.sport}</Chip>
                <Chip>{t.league}</Chip>
                <Chip tone="dark">Chrome</Chip>
                <span style={{ fontSize: 12, color: '#6B6757', marginLeft: 6 }}>
                  {t.athletes} athletes featured in this set
                </span>
              </div>
            </div>

            {/* Roster summary panel */}
            <RosterSummary t={t}/>
          </div>
        </div>

        {/* STAT STRIP — 4 team totals */}
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
          background: '#FFFFFF', borderBottom: '1px solid #EDEAE0',
        }}>
          {[
            ['ATHLETES', t.athletes.toString()],
            ['TOTAL CARDS', t.totalCards.toLocaleString()],
            ['NUMBERED PARALLELS', t.numberedParallels.toLocaleString()],
            ['1/1S', t.oneOfOnes.toString()],
          ].map(([label, val], i) => (
            <div key={label} style={{
              padding: '18px 22px',
              borderRight: i < 3 ? '1px solid #EDEAE0' : 'none',
            }}>
              <div style={{
                fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
              }}>{label}</div>
              <div style={{
                fontFamily: '"Inter Tight", Inter, sans-serif',
                fontSize: 26, fontWeight: 600, letterSpacing: -0.6, color: '#0F0F0E',
                marginTop: 4,
              }}>{val}</div>
            </div>
          ))}
        </div>

        {/* PRIMARY TABS */}
        <div style={{
          display: 'flex', gap: 0, padding: '0 36px',
          background: '#FAFAF7', borderBottom: '1px solid #EDEAE0',
        }}>
          {tabs.map((tb) => (
            <button key={tb} onClick={() => setTab(tb)} style={{
              padding: '14px 20px', background: 'none', border: 'none',
              borderBottom: tab === tb ? '2px solid #0F0F0E' : '2px solid transparent',
              marginBottom: -1, color: tab === tb ? '#0F0F0E' : '#8A8677',
              fontFamily: 'inherit', fontSize: 13,
              fontWeight: tab === tb ? 600 : 500, cursor: 'pointer',
            }}>{tb}</button>
          ))}
        </div>

        {/* CONTENT */}
        <main style={{ padding: '24px 36px 60px' }}>
          {/* Filter bar — visible on Athletes tab */}
          {(tab === 'Athletes' || tab === 'Overview') && (
            <div style={{
              display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14,
              flexWrap: 'wrap',
            }}>
              <div style={{
                fontFamily: '"Inter Tight", Inter, sans-serif',
                fontSize: 16, fontWeight: 600, letterSpacing: -0.3, color: '#0F0F0E',
                marginRight: 'auto',
              }}>Athletes ({sorted.length})</div>
              <Select label="POSITION" value={position} onChange={setPosition} options={positions}/>
              <label style={{
                display: 'inline-flex', alignItems: 'center', gap: 6,
                fontSize: 12, color: '#3A372F', cursor: 'pointer',
              }}>
                <input type="checkbox" checked={rookiesOnly}
                  onChange={(e) => setRookiesOnly(e.target.checked)}
                  style={{ accentColor: '#0F0F0E' }}/>
                Rookies only
              </label>
            </div>
          )}

          {(tab === 'Athletes' || tab === 'Overview') && (
            <AthletesTable rows={sorted} sort={sort} setSort={setSort}/>
          )}

          {tab === 'Inserts' && (
            <PlaceholderTab label="Inserts breakdown by athlete — coming soon"/>
          )}
          {tab === 'Autographs' && (
            <PlaceholderTab label="Autograph breakdown by athlete — coming soon"/>
          )}
          {tab === 'Numbered Parallels' && (
            <PlaceholderTab label="Numbered parallel breakdown by athlete — coming soon"/>
          )}
        </main>
      </div>
    </div>
  );
}

// ─── Sub-components ────────────────────────────────────────────────────────

function TeamCrest({ name, primary, secondary, size = 64 }) {
  // Brand-tinted geometric crest tile, used in hero + rail
  const initials = (name || '').slice(0, 2).toUpperCase();
  return (
    <div style={{
      width: size, height: size, position: 'relative',
      background: primary, overflow: 'hidden', flex: '0 0 auto',
      border: size >= 80 ? '1px solid #EDEAE0' : 'none',
    }}>
      <div style={{
        position: 'absolute', inset: 0,
        background: `linear-gradient(135deg, ${primary} 0%, ${primary} 55%, ${secondary} 55%, ${secondary} 100%)`,
      }}/>
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage: 'repeating-linear-gradient(45deg, rgba(255,255,255,0.06) 0 2px, transparent 2px 8px)',
      }}/>
      <div style={{
        position: 'absolute', inset: 0, display: 'flex',
        alignItems: 'center', justifyContent: 'center',
        fontFamily: '"Inter Tight", Inter, sans-serif',
        fontSize: size >= 120 ? 64 : size >= 60 ? 22 : 12,
        fontWeight: 700, letterSpacing: size >= 120 ? -2 : -0.5,
        color: '#FFFFFF', textShadow: '0 1px 2px rgba(0,0,0,0.25)',
      }}>{initials}</div>
      {size >= 120 && (
        <>
          <div style={{
            position: 'absolute', top: 10, left: 10,
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize: 9, letterSpacing: 1.6, color: 'rgba(255,255,255,0.8)', fontWeight: 600,
          }}>CREST</div>
          <div style={{
            position: 'absolute', bottom: 10, left: 10, right: 10,
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize: 9, letterSpacing: 1.4, color: 'rgba(255,255,255,0.8)', fontWeight: 600,
            display: 'flex', justifyContent: 'space-between',
          }}>
            <span>{name.toUpperCase()}</span>
            <span>API</span>
          </div>
        </>
      )}
    </div>
  );
}

function RosterSummary({ t }) {
  return (
    <div style={{
      background: '#FAFAF7',
      padding: '14px 16px',
      border: '2px solid #F2F0E9',
    }}>
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        marginBottom: 10,
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
        fontFamily: '"Inter Tight", Inter, sans-serif',
        fontSize: 15, fontWeight: 600, letterSpacing: -0.2, color: '#0F0F0E',
        marginBottom: 8,
      }}>{t.team}</div>
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
          padding: '4px 0', fontSize: 11, color: '#3A372F',
        }}>
          <span>{k}</span>
          <span style={{
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontWeight: 600, color: '#0F0F0E',
          }}>{v}</span>
        </div>
      ))}
    </div>
  );
}

function Select({ label, value, onChange, options }) {
  return (
    <div>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#8A8677', fontWeight: 600,
        marginBottom: 4,
      }}>{label}</div>
      <div style={{
        position: 'relative',
        border: '1px solid #E6E3D9', borderRadius: 6, background: '#FFFFFF',
      }}>
        <select value={value} onChange={(e) => onChange(e.target.value)} style={{
          appearance: 'none', WebkitAppearance: 'none',
          background: 'transparent', border: 'none', outline: 'none',
          padding: '7px 28px 7px 10px', fontSize: 12, fontFamily: 'inherit',
          color: '#0F0F0E', cursor: 'pointer', minWidth: 160,
        }}>
          {options.map((o) => <option key={o} value={o}>{o}</option>)}
        </select>
        <span style={{
          position: 'absolute', right: 10, top: '50%',
          transform: 'translateY(-50%)', pointerEvents: 'none',
          display: 'inline-flex',
        }}>
          <IconChev dir="down" size={11} color="#6B6757"/>
        </span>
      </div>
    </div>
  );
}

function AthletesTable({ rows, sort, setSort }) {
  const cols = '32px 2fr 70px 90px 110px 90px 130px';
  const headers = [
    { key: '_rank',             label: '#',                  align: 'left',  sortable: false },
    { key: 'name',              label: 'ATHLETE',            align: 'left',  sortable: true },
    { key: 'position',          label: 'POS',                align: 'left',  sortable: true },
    { key: 'totalCards',        label: 'TOTAL CARDS',        align: 'right', sortable: true },
    { key: 'autographs',        label: 'AUTOGRAPHS',         align: 'right', sortable: true },
    { key: 'inserts',           label: 'INSERTS',            align: 'right', sortable: true },
    { key: 'numberedParallels', label: 'NUMBERED PARALLELS', align: 'right', sortable: true },
  ];

  function clickHeader(key, sortable) {
    if (!sortable) return;
    if (sort.key === key) {
      setSort({ key, dir: sort.dir === 'asc' ? 'desc' : 'asc' });
    } else {
      setSort({ key, dir: typeof rows[0]?.[key] === 'string' ? 'asc' : 'desc' });
    }
  }

  return (
    <div style={{
      background: '#FFFFFF', border: '1px solid #EDEAE0',
    }}>
      <div style={{
        fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize: 9, letterSpacing: 1.6, color: '#6B6757', fontWeight: 600,
        padding: '12px 18px', borderBottom: '1px solid #EDEAE0',
        display: 'grid', gridTemplateColumns: cols, gap: 12, background: '#FAFAF7',
      }}>
        {headers.map((h) => {
          const active = sort.key === h.key;
          return (
            <span key={h.key} onClick={() => clickHeader(h.key, h.sortable)} style={{
              textAlign: h.align, cursor: h.sortable ? 'pointer' : 'default',
              color: active ? '#0F0F0E' : '#6B6757',
              userSelect: 'none',
              display: 'inline-flex', gap: 4,
              justifyContent: h.align === 'right' ? 'flex-end' : 'flex-start',
              alignItems: 'center',
            }}>
              {h.label}
              {h.sortable && active && (
                <span style={{ fontSize: 9 }}>{sort.dir === 'asc' ? '▲' : '▼'}</span>
              )}
            </span>
          );
        })}
      </div>
      {rows.map((a, i) => (
        <a key={a.rank} href="#" style={{
          display: 'grid', gridTemplateColumns: cols, gap: 12,
          padding: '14px 18px',
          borderBottom: i < rows.length - 1 ? '1px solid #F4F1E8' : 'none',
          fontSize: 13, color: '#0F0F0E', alignItems: 'center',
          textDecoration: 'none',
        }}>
          <span style={{
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize: 11, color: '#8A8677',
          }}>{a.rank}</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{
              width: 30, height: 30, borderRadius: '50%', background: '#EAE6D9',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 10, fontWeight: 600, color: '#6B6757', flex: '0 0 auto',
            }}>{a.name.split(' ').map((p) => p[0]).join('').slice(0, 2)}</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, minWidth: 0 }}>
              <span style={{ fontWeight: 600, color: '#0F0F0E' }}>{a.name}</span>
              {a.rookie && <span style={{
                fontSize: 9, fontWeight: 700, padding: '1px 5px', borderRadius: 2,
                background: 'oklch(0.55 0.17 25)', color: '#FFF8F1', letterSpacing: 0.6,
              }}>RC</span>}
            </div>
          </div>
          <span style={{ color: '#3A372F' }}>{a.position}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontWeight: 600,
          }}>{a.totalCards.toLocaleString()}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            color: a.autographs === 0 ? '#B7B2A3' : '#3A372F',
          }}>{a.autographs === 0 ? '—' : a.autographs}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            color: '#3A372F',
          }}>{a.inserts}</span>
          <span style={{
            textAlign: 'right',
            fontFamily: 'ui-monospace, "JetBrains Mono", Menlo, monospace',
            color: '#3A372F',
          }}>{a.numberedParallels.toLocaleString()}</span>
        </a>
      ))}
    </div>
  );
}

function PlaceholderTab({ label }) {
  return (
    <div style={{
      background: '#FFFFFF', border: '1px dashed #E6E3D9',
      padding: '40px 24px', textAlign: 'center',
      fontSize: 13, color: '#8A8677',
    }}>{label}</div>
  );
}

window.TeamDetailD = TeamDetailD;
