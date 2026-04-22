// Main App — orchestrates state, routing between index/detail, filters, Tweaks host.

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "density": 5,
  "showMeta": true
}/*EDITMODE-END*/;

function App() {
  const [view, setView] = React.useState(() => localStorage.getItem('cl_view') || 'gallery');
  const [sport, setSport] = React.useState('all');
  const [query, setQuery] = React.useState('');
  const [openId, setOpenId] = React.useState(() => localStorage.getItem('cl_openId') || null);
  const [tweaks, setTweaks] = React.useState(TWEAK_DEFAULTS);
  const [tweaksOpen, setTweaksOpen] = React.useState(false);

  React.useEffect(()=>{ localStorage.setItem('cl_view', view); }, [view]);
  React.useEffect(()=>{
    if (openId) localStorage.setItem('cl_openId', openId);
    else localStorage.removeItem('cl_openId');
  }, [openId]);

  // Tweaks host protocol
  React.useEffect(() => {
    function onMsg(e) {
      if (!e.data) return;
      if (e.data.type === '__activate_edit_mode') setTweaksOpen(true);
      if (e.data.type === '__deactivate_edit_mode') setTweaksOpen(false);
    }
    window.addEventListener('message', onMsg);
    window.parent.postMessage({type:'__edit_mode_available'}, '*');
    return () => window.removeEventListener('message', onMsg);
  }, []);

  function updateTweaks(patch) {
    const next = { ...tweaks, ...patch };
    setTweaks(next);
    window.parent.postMessage({type:'__edit_mode_set_keys', edits: patch}, '*');
  }

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
    <div style={{
      minHeight:'100vh',
      background:'#FAFAF7',
      fontFamily:'Inter, system-ui, -apple-system, sans-serif',
      color:'#0F0F0E',
    }}>
      <div style={{
        maxWidth: 1440, margin:'0 auto',
        padding: '40px 56px 80px',
      }}>
        {openSet ? (
          <SetDetail set={openSet} onBack={()=>setOpenId(null)}/>
        ) : (
          <div data-screen-label="Checklists Index">
            <PageHeader/>
            <SportFilter active={sport} onChange={setSport}/>
            <SearchAndView query={query} onQuery={setQuery} view={view} onView={setView}/>

            <div style={{marginTop:36, display:'flex', alignItems:'baseline', gap:12}}>
              <span style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:10, letterSpacing:2, color:'#0F0F0E', fontWeight:600,
              }}>
                {sport==='all' ? 'ALL SETS' : window.SPORTS.find(s=>s.id===sport).label.toUpperCase()}
              </span>
              <span style={{
                fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
                fontSize:10, letterSpacing:2, color:'#B7B2A3', fontWeight:500,
              }}>{filtered.length} {filtered.length===1?'SET':'SETS'}{query && ` MATCHING "${query.toUpperCase()}"`}</span>
            </div>

            <div style={{marginTop:18}}>
              {filtered.length === 0 ? (
                <div style={{
                  padding:'80px 20px', textAlign:'center',
                  border:'1px dashed #D9D5C7', borderRadius:12,
                  color:'#8A8677',
                }}>
                  <div style={{fontSize:14, marginBottom:6, color:'#3A372F', fontWeight:500}}>No sets match your filters.</div>
                  <div style={{fontSize:12}}>Try clearing the search or picking a different sport.</div>
                </div>
              ) : view==='gallery' ? (
                <GalleryView sets={filtered} onOpen={setOpenId} showMeta={tweaks.showMeta} density={tweaks.density}/>
              ) : (
                <CompactView sets={filtered} onOpen={setOpenId} showMeta={tweaks.showMeta}/>
              )}
            </div>
          </div>
        )}
      </div>

      <TweaksPanel
        state={tweaks}
        onChange={updateTweaks}
        visible={tweaksOpen}
        onClose={()=>{
          setTweaksOpen(false);
          window.parent.postMessage({type:'__edit_mode_deactivate_request'}, '*');
        }}
      />
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App/>);
