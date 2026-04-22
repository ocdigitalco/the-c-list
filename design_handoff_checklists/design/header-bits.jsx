// Header, filters, search, view toggle, featured strip

function PageHeader() {
  return (
    <div>
      <button style={{
        display:'inline-flex', alignItems:'center', gap:6,
        background:'none', border:'none', padding:0, cursor:'pointer',
        color:'#6B6757', fontSize:13, fontFamily:'inherit',
      }}>
        <IconChev dir="left" size={12} color="#6B6757" />
        Home
      </button>
      <h1 style={{
        fontFamily:'"Inter Tight", Inter, system-ui, sans-serif',
        fontSize: 48, fontWeight: 600, letterSpacing: -1.2,
        margin:'14px 0 8px', color:'#0F0F0E', lineHeight:1,
      }}>
        Checklists
      </h1>
      <p style={{ color:'#6B6757', fontSize:14, margin:0 }}>
        Browse all sports card sets in the app
      </p>
    </div>
  );
}

function SportFilter({ active, onChange }) {
  const scrollRef = React.useRef(null);
  return (
    <div style={{display:'flex', alignItems:'center', gap:16, marginTop:32}}>
      <div style={{
        fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize:10, letterSpacing:2, color:'#8A8677', fontWeight:500,
      }}>SPORT</div>
      <div ref={scrollRef} style={{
        display:'flex', gap:4, overflowX:'auto', flex:1,
        scrollbarWidth:'none', msOverflowStyle:'none',
      }} className="no-scrollbar">
        {window.SPORTS.map(s => {
          const isActive = s.id === active;
          return (
            <button key={s.id} onClick={()=>onChange(s.id)}
              style={{
                flex:'0 0 auto',
                padding: isActive ? '8px 16px' : '8px 14px',
                borderRadius: 999,
                border: isActive ? '1px solid #0F0F0E' : '1px solid transparent',
                background: isActive ? '#0F0F0E' : 'transparent',
                color: isActive ? '#FAFAF7' : '#3A372F',
                fontFamily:'inherit', fontSize:13,
                fontWeight: isActive ? 500 : 400,
                cursor:'pointer',
                transition:'all 0.15s ease',
                whiteSpace:'nowrap',
              }}
              onMouseEnter={e=>{ if(!isActive) e.currentTarget.style.background='#F1EFE9'; }}
              onMouseLeave={e=>{ if(!isActive) e.currentTarget.style.background='transparent'; }}
            >
              {s.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function SearchAndView({ query, onQuery, view, onView }) {
  return (
    <div style={{display:'flex', gap:8, marginTop:20}}>
      <div style={{
        flex:1, position:'relative',
        background:'#F1EFE9', borderRadius:10,
        display:'flex', alignItems:'center', padding:'0 16px',
        height:48,
      }}>
        <IconSearch />
        <input
          value={query}
          onChange={e=>onQuery(e.target.value)}
          placeholder="Search by name, sport, league, or tier..."
          style={{
            flex:1, border:'none', background:'transparent', outline:'none',
            padding:'0 12px', fontSize:14, color:'#0F0F0E',
            fontFamily:'inherit',
          }}
        />
        {query && (
          <button onClick={()=>onQuery('')} style={{
            background:'none', border:'none', cursor:'pointer', padding:4,
            display:'flex', alignItems:'center',
          }}>
            <IconX size={14} color="#6B6757" />
          </button>
        )}
      </div>
      <div style={{display:'flex', gap:4, background:'#F1EFE9', borderRadius:10, padding:4}}>
        <button onClick={()=>onView('gallery')} style={{
          width:40, height:40, borderRadius:7, border:'none',
          background: view==='gallery' ? '#0F0F0E' : 'transparent',
          display:'flex', alignItems:'center', justifyContent:'center', cursor:'pointer',
          transition:'background 0.15s',
        }} aria-label="Gallery view">
          <IconGrid color={view==='gallery' ? '#FAFAF7' : '#1A1916'} />
        </button>
        <button onClick={()=>onView('compact')} style={{
          width:40, height:40, borderRadius:7, border:'none',
          background: view==='compact' ? '#0F0F0E' : 'transparent',
          display:'flex', alignItems:'center', justifyContent:'center', cursor:'pointer',
          transition:'background 0.15s',
        }} aria-label="Compact view">
          <IconRows color={view==='compact' ? '#FAFAF7' : '#1A1916'} />
        </button>
      </div>
    </div>
  );
}

function FeaturedStrip({ sets, onOpen }) {
  const featured = sets.filter(s => s.featured).slice(0, 4);
  if (featured.length === 0) return null;
  // Deterministic collector counts + % change, seeded by set id
  const stats = featured.map((s, i) => {
    const h = [...s.id].reduce((a,c)=>a+c.charCodeAt(0),0);
    const collectors = 1200 + (h * 37) % 8600;
    const trend = 4 + (h * 13) % 36;
    return { collectors, trend };
  });
  return (
    <div style={{marginTop:36}}>
      <div style={{display:'flex', alignItems:'baseline', justifyContent:'space-between', marginBottom:14}}>
        <div style={{display:'flex', alignItems:'baseline', gap:10}}>
          <span style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:10, letterSpacing:2, color:'#0F0F0E', fontWeight:600,
          }}>TRENDING SETS</span>
          <span style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:10, letterSpacing:2, color:'#B7B2A3', fontWeight:500,
          }}>MOST COLLECTED THIS WEEK</span>
        </div>
        <a style={{
          fontSize:12, color:'#6B6757', textDecoration:'none', cursor:'pointer',
          display:'inline-flex', alignItems:'center', gap:4,
        }}>View all <IconChev dir="right" size={10} color="#6B6757"/></a>
      </div>
      <div style={{
        display:'grid',
        gridTemplateColumns:`repeat(${featured.length}, 1fr)`,
        gap:20,
      }}>
        {featured.map((s, i) => (
          <div key={s.id} onClick={()=>onOpen(s.id)} style={{
            cursor:'pointer',
          }} className="feat-tile">
            <div style={{
              position:'relative', overflow:'hidden',
              aspectRatio:'2.5 / 3.5',
              background:'#0F0F0E',
              boxShadow:'0 1px 2px rgba(15,15,14,0.08)',
            }}>
              <div style={{position:'absolute', inset:0}}>
                <CardArt set={s} width={300} height={420} />
              </div>
              <div style={{position:'absolute', top:12, left:12, display:'flex', gap:6}}>
                <span style={{
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  fontSize:10, letterSpacing:1.5, color:'#FAFAF7', fontWeight:600,
                  background:'rgba(0,0,0,0.5)', padding:'4px 8px', borderRadius:3,
                  backdropFilter:'blur(4px)',
                }}>#{i+1}</span>
              </div>
              <div style={{
                position:'absolute', top:12, right:12,
                display:'inline-flex', alignItems:'center', gap:3,
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:10, letterSpacing:0.5, fontWeight:600,
                color:'#FAFAF7',
                background:'rgba(0,0,0,0.5)', padding:'4px 8px', borderRadius:3,
                backdropFilter:'blur(4px)',
              }}>
                <svg width="8" height="8" viewBox="0 0 8 8"><path d="M4 1L7 6H1z" fill="#9AE07A"/></svg>
                {stats[i].trend}%
              </div>
            </div>
            <div style={{paddingTop:12}}>
              <div style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:9, letterSpacing:2, color:'#8A8677', marginBottom:4, fontWeight:500,
              }}>
                {(s.leagues[0]||'').toUpperCase()} · {s.tiers[0]?.toUpperCase() || 'BASE'}
              </div>
              <div style={{
                fontFamily:'"Inter Tight", Inter, sans-serif',
                fontSize:15, fontWeight:600, letterSpacing:-0.3, color:'#0F0F0E',
                lineHeight:1.2,
              }}>{s.name}</div>
              <div style={{
                display:'flex', gap:10, marginTop:8,
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:11, color:'#6B6757',
              }}>
                <span>{stats[i].collectors.toLocaleString()} <span style={{color:'#B7B2A3'}}>collectors</span></span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

Object.assign(window, { PageHeader, SportFilter, SearchAndView, FeaturedStrip });
