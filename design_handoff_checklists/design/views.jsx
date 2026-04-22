// Gallery view (image-forward grid) + Compact view (thumbnail list)

function GalleryCard({ set, onOpen, showMeta, density }) {
  const [hover, setHover] = React.useState(false);
  const aspect = density === 6 ? '2/2.8' : '2/2.8';
  return (
    <div
      onClick={()=>onOpen(set.id)}
      onMouseEnter={()=>setHover(true)}
      onMouseLeave={()=>setHover(false)}
      style={{ cursor:'pointer' }}
    >
      <div style={{
        aspectRatio: aspect,
        borderRadius: 0,
        overflow:'hidden',
        background:'#EAE6D9',
        position:'relative',
        transform: hover ? 'translateY(-2px)' : 'translateY(0)',
        boxShadow: hover ? '0 12px 28px rgba(15,15,14,0.16)' : '0 1px 2px rgba(15,15,14,0.06)',
        transition:'all 0.2s ease',
      }}>
        <CardArt set={set} width={300} height={420} />
        {set.featured && (
          <div style={{
            position:'absolute', top:10, left:-4,
            background:'oklch(0.55 0.17 25)', color:'#FFF8F1',
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:9, letterSpacing:1.5, fontWeight:700,
            padding:'4px 8px 4px 10px',
            boxShadow:'0 2px 6px rgba(0,0,0,0.18)',
            clipPath:'polygon(0 0, 100% 0, 100% 100%, 0 100%, 4px 50%)',
          }}>RECENTLY ADDED</div>
        )}
        {hover && (
          <div style={{
            position:'absolute', inset:0,
            background:'linear-gradient(to top, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 50%)',
            display:'flex', alignItems:'flex-end', padding:12,
          }}>
            <span style={{
              color:'#FAFAF7', fontSize:11,
              fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
              letterSpacing:1.5, fontWeight:600,
            }}>
              OPEN CHECKLIST →
            </span>
          </div>
        )}
      </div>
      {showMeta && (
        <div style={{paddingTop:12}}>
          <div style={{
            fontFamily:'"Inter Tight", Inter, sans-serif',
            fontSize:14, fontWeight:600, color:'#0F0F0E', letterSpacing:-0.2,
            lineHeight:1.3,
          }}>{set.name}</div>
          <div style={{display:'flex', gap:5, marginTop:8, flexWrap:'wrap'}}>
            {set.leagues.slice(0,1).map(l=>(<Chip key={l}>{l}</Chip>))}
            {set.tiers.slice(0,1).map(t=>(<Chip key={t} tone="dark">{t}</Chip>))}
          </div>
          <div style={{display:'flex', gap:14, marginTop:10, fontSize:11, color:'#6B6757',
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
          }}>
            <span>{set.athletes} <span style={{color:'#B7B2A3'}}>athletes</span></span>
            <span>{set.cards.toLocaleString()} <span style={{color:'#B7B2A3'}}>cards</span></span>
          </div>
        </div>
      )}
    </div>
  );
}

function GalleryView({ sets, onOpen, showMeta, density }) {
  return (
    <div style={{
      display:'grid',
      gridTemplateColumns:`repeat(${density}, minmax(0, 1fr))`,
      gap: density >= 6 ? 14 : 20,
      rowGap: showMeta ? (density >= 6 ? 28 : 36) : 14,
    }}>
      {sets.map(s => (
        <GalleryCard key={s.id} set={s} onOpen={onOpen} showMeta={showMeta} density={density}/>
      ))}
    </div>
  );
}

function CompactRow({ set, onOpen, showMeta }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div
      onClick={()=>onOpen(set.id)}
      onMouseEnter={()=>setHover(true)}
      onMouseLeave={()=>setHover(false)}
      style={{
        display:'flex', alignItems:'center', gap:18,
        padding:'14px 16px',
        border:'1px solid #EDEAE0',
        borderRadius:10,
        background: hover ? '#FDFCF8' : '#FFFFFF',
        cursor:'pointer',
        transition:'all 0.15s',
        boxShadow: hover ? '0 4px 14px rgba(15,15,14,0.06)' : 'none',
      }}
    >
      <div style={{
        width:80, height:112, borderRadius:0, overflow:'hidden',
        flex:'0 0 auto', background:'#EAE6D9', position:'relative',
        boxShadow: '0 1px 2px rgba(15,15,14,0.08)',
      }}>
        <CardArt set={set} width={80} height={112}/>
        {set.featured && (
          <div style={{
            position:'absolute', top:6, left:-3,
            background:'oklch(0.55 0.17 25)', color:'#FFF8F1',
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:7, letterSpacing:1, fontWeight:700,
            padding:'2px 5px 2px 6px',
            clipPath:'polygon(0 0, 100% 0, 100% 100%, 0 100%, 3px 50%)',
          }}>NEW</div>
        )}
      </div>
      <div style={{flex:1, minWidth:0}}>
        <div style={{
          fontFamily:'"Inter Tight", Inter, sans-serif',
          fontSize:15, fontWeight:600, color:'#0F0F0E', letterSpacing:-0.2,
        }}>{set.name}</div>
        {showMeta && (
          <div style={{display:'flex', gap:6, marginTop:8, flexWrap:'wrap'}}>
            {set.leagues.slice(0,1).map(l=>(<Chip key={l}>{l}</Chip>))}
            {set.tiers.slice(0,1).map(t=>(<Chip key={t} tone="dark">{t}</Chip>))}
          </div>
        )}
      </div>
      {showMeta && (
        <>
          <div style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:12, color:'#6B6757', width:110,
          }}>
            <div style={{color:'#0F0F0E', fontWeight:600}}>{set.athletes}</div>
            <div style={{fontSize:10, color:'#B7B2A3', letterSpacing:1}}>ATHLETES</div>
          </div>
          <div style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:12, color:'#6B6757', width:110,
          }}>
            <div style={{color:'#0F0F0E', fontWeight:600}}>{set.cards.toLocaleString()}</div>
            <div style={{fontSize:10, color:'#B7B2A3', letterSpacing:1}}>CARDS</div>
          </div>
          <div style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:12, color:'#6B6757', width:60,
          }}>
            <div style={{color:'#0F0F0E', fontWeight:600}}>{set.year}</div>
            <div style={{fontSize:10, color:'#B7B2A3', letterSpacing:1}}>YEAR</div>
          </div>
        </>
      )}
      <IconChev dir="right" size={14} color="#B7B2A3"/>
    </div>
  );
}

function CompactView({ sets, onOpen, showMeta }) {
  return (
    <div style={{display:'flex', flexDirection:'column', gap:8}}>
      {sets.map(s => <CompactRow key={s.id} set={s} onOpen={onOpen} showMeta={showMeta}/>)}
    </div>
  );
}

Object.assign(window, { GalleryView, CompactView });
