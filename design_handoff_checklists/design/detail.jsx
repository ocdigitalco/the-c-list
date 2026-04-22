// Set detail screen (full-page takeover with back button)

function SetDetail({ set, onBack }) {
  const [tab, setTab] = React.useState('Base');
  const tabs = ['Base', 'Inserts', 'Parallels', 'Autographs', 'Relics'];

  // Generate fake checklist cards deterministically
  const names = ['K. Owens', 'M. Reyes', 'T. Abara', 'J. Sato', 'L. Kovacs', 'R. Bakr', 'D. Njoku', 'A. Volkov',
    'C. Park', 'S. Marquez', 'B. Haruna', 'N. Okafor', 'P. Weiss', 'E. Tomori', 'V. Singh', 'H. Lindqvist',
    'W. Banda', 'F. Aoki', 'Y. Ferrari', 'R. Moreau', 'I. Dembele', 'G. Brambilla', 'Z. Hargrave', 'Q. Bellingham'];
  const cards = names.slice(0, 24).map((n, i) => ({
    num: String(i+1).padStart(3,'0'),
    name: n,
    team: ['North','South','East','West'][i%4] + ' ' + ['Apex','Vanguard','Heritage','Legion'][i%4],
    variant: i%7===0 ? 'SP' : (i%5===0 ? 'RC' : ''),
  }));

  return (
    <div style={{
      animation: 'fadeInUp 0.3s ease',
      paddingTop:24,
    }}>
      <button onClick={onBack} style={{
        display:'inline-flex', alignItems:'center', gap:6,
        background:'none', border:'none', padding:'8px 12px 8px 0',
        cursor:'pointer', color:'#6B6757', fontSize:13, fontFamily:'inherit',
      }}>
        <IconChev dir="left" size={12} color="#6B6757" />
        Checklists
      </button>

      <div style={{
        display:'grid', gridTemplateColumns:'340px 1fr', gap:48,
        marginTop:20, alignItems:'start',
      }}>
        {/* Left: hero card + metadata */}
        <div style={{position:'sticky', top:24}}>
          <div style={{
            width:'100%', aspectRatio:'2/2.8', borderRadius:12, overflow:'hidden',
            background:'#EAE6D9', boxShadow:'0 24px 60px rgba(15,15,14,0.18), 0 2px 4px rgba(15,15,14,0.08)',
          }}>
            <CardArt set={set} width={340} height={476}/>
          </div>

          <div style={{marginTop:28}}>
            <div style={{
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              fontSize:10, letterSpacing:2, color:'#8A8677', fontWeight:500,
            }}>{(set.leagues[0]||'').toUpperCase()} · {set.year}</div>
            <h2 style={{
              fontFamily:'"Inter Tight", Inter, sans-serif',
              fontSize:32, fontWeight:600, letterSpacing:-0.8,
              margin:'8px 0 0', color:'#0F0F0E', lineHeight:1.1,
            }}>{set.name}</h2>

            <div style={{display:'flex', gap:6, marginTop:14, flexWrap:'wrap'}}>
              {set.leagues.map(l=>(<Chip key={l}>{l}</Chip>))}
              {set.tiers.map(t=>(<Chip key={t} tone="dark">{t}</Chip>))}
            </div>

            <div style={{
              display:'grid', gridTemplateColumns:'1fr 1fr', gap:1,
              marginTop:24, background:'#EDEAE0', borderRadius:8, overflow:'hidden',
            }}>
              <Stat label="ATHLETES" value={set.athletes}/>
              <Stat label="TOTAL CARDS" value={set.cards.toLocaleString()}/>
              <Stat label="RELEASE" value={set.year}/>
              <Stat label="SERIES" value={(set.tiers[0] || 'Base').toUpperCase()}/>
            </div>

            <button style={{
              width:'100%', marginTop:20, padding:'14px 16px',
              background:'#0F0F0E', color:'#FAFAF7', border:'none',
              borderRadius:10, fontFamily:'inherit', fontSize:14, fontWeight:500,
              cursor:'pointer', letterSpacing:-0.1,
            }}>Track my collection</button>
            <button style={{
              width:'100%', marginTop:8, padding:'14px 16px',
              background:'transparent', color:'#0F0F0E',
              border:'1px solid #D9D5C7',
              borderRadius:10, fontFamily:'inherit', fontSize:14, fontWeight:500,
              cursor:'pointer',
            }}>Export checklist</button>
          </div>
        </div>

        {/* Right: checklist */}
        <div>
          <div style={{
            display:'flex', gap:4, borderBottom:'1px solid #EDEAE0',
            marginBottom:20,
          }}>
            {tabs.map(t => (
              <button key={t} onClick={()=>setTab(t)} style={{
                padding:'12px 18px',
                background:'none', border:'none',
                borderBottom: tab===t ? '2px solid #0F0F0E' : '2px solid transparent',
                marginBottom:-1,
                color: tab===t ? '#0F0F0E' : '#8A8677',
                fontFamily:'inherit', fontSize:13,
                fontWeight: tab===t ? 600 : 400,
                cursor:'pointer',
              }}>{t}</button>
            ))}
          </div>

          <div style={{
            display:'grid', gridTemplateColumns:'60px 1fr 1fr 80px 40px',
            gap:0, padding:'0 14px 10px',
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:10, letterSpacing:1.5, color:'#B7B2A3', fontWeight:500,
            borderBottom:'1px solid #EDEAE0',
          }}>
            <div>#</div>
            <div>ATHLETE</div>
            <div>TEAM</div>
            <div>VARIANT</div>
            <div></div>
          </div>

          <div>
            {cards.map((c, i) => (
              <div key={c.num} style={{
                display:'grid', gridTemplateColumns:'60px 1fr 1fr 80px 40px',
                gap:0, padding:'14px', alignItems:'center',
                borderBottom:'1px solid #F4F1E8',
                fontSize:14, color:'#0F0F0E',
              }}
              onMouseEnter={e=>e.currentTarget.style.background='#FAF8F1'}
              onMouseLeave={e=>e.currentTarget.style.background='transparent'}
              >
                <div style={{
                  fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                  color:'#8A8677', fontSize:12,
                }}>{c.num}</div>
                <div style={{fontWeight:500}}>{c.name}</div>
                <div style={{color:'#6B6757'}}>{c.team}</div>
                <div>
                  {c.variant && <Chip tone={c.variant==='SP'?'accent':'default'}>{c.variant}</Chip>}
                </div>
                <div style={{textAlign:'right'}}>
                  <input type="checkbox"
                    defaultChecked={i%4===0}
                    style={{width:18, height:18, accentColor:'#0F0F0E', cursor:'pointer'}}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div style={{background:'#FAFAF7', padding:'16px 18px'}}>
      <div style={{
        fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
        fontSize:10, letterSpacing:1.5, color:'#B7B2A3', fontWeight:500,
      }}>{label}</div>
      <div style={{
        fontFamily:'"Inter Tight", Inter, sans-serif',
        fontSize:22, fontWeight:600, color:'#0F0F0E',
        letterSpacing:-0.5, marginTop:4,
      }}>{value}</div>
    </div>
  );
}

window.SetDetail = SetDetail;
