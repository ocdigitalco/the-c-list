// Tweaks floating panel — grid density + show/hide metadata

function TweaksPanel({ state, onChange, visible, onClose }) {
  if (!visible) return null;
  return (
    <div style={{
      position:'fixed', right:20, bottom:20,
      width:280, background:'#FFFFFF',
      border:'1px solid #E6E3D9',
      borderRadius:14, overflow:'hidden',
      boxShadow:'0 16px 40px rgba(15,15,14,0.18)',
      fontFamily:'inherit',
      zIndex:1000,
      animation:'fadeInUp 0.2s ease',
    }}>
      <div style={{
        display:'flex', alignItems:'center', justifyContent:'space-between',
        padding:'14px 16px', borderBottom:'1px solid #EDEAE0',
      }}>
        <div style={{display:'flex', alignItems:'center', gap:8}}>
          <IconSliders/>
          <span style={{
            fontFamily:'"Inter Tight", Inter, sans-serif',
            fontSize:13, fontWeight:600, letterSpacing:-0.1,
          }}>Tweaks</span>
        </div>
        <button onClick={onClose} style={{
          background:'none', border:'none', cursor:'pointer', padding:4,
          display:'flex', alignItems:'center',
        }}>
          <IconX size={14} color="#6B6757"/>
        </button>
      </div>

      <div style={{padding:'16px'}}>
        <div>
          <label style={{
            fontFamily:'ui-monospace, "JetBrains Mono", Menlo, monospace',
            fontSize:10, letterSpacing:1.5, color:'#8A8677', fontWeight:500,
            display:'block', marginBottom:8,
          }}>GALLERY DENSITY</label>
          <div style={{display:'flex', gap:4}}>
            {[4, 5, 6].map(d => (
              <button key={d} onClick={()=>onChange({density:d})}
                style={{
                  flex:1, padding:'8px 0',
                  background: state.density===d ? '#0F0F0E' : '#F4F1E8',
                  color: state.density===d ? '#FAFAF7' : '#3A372F',
                  border:'none', borderRadius:6,
                  fontFamily:'inherit', fontSize:12, fontWeight:500,
                  cursor:'pointer',
                }}
              >{d} across</button>
            ))}
          </div>
        </div>

        <div style={{marginTop:18, display:'flex', alignItems:'center', justifyContent:'space-between'}}>
          <div>
            <div style={{fontSize:13, color:'#0F0F0E', fontWeight:500}}>Show metadata</div>
            <div style={{fontSize:11, color:'#8A8677', marginTop:2}}>Tiers, counts, and labels</div>
          </div>
          <button onClick={()=>onChange({showMeta: !state.showMeta})} style={{
            width:40, height:22, borderRadius:999,
            background: state.showMeta ? '#0F0F0E' : '#D9D5C7',
            border:'none', position:'relative', cursor:'pointer',
            transition:'background 0.15s',
          }}>
            <div style={{
              position:'absolute', top:2, left: state.showMeta ? 20 : 2,
              width:18, height:18, borderRadius:999,
              background:'#FFFFFF',
              transition:'left 0.15s',
              boxShadow:'0 1px 2px rgba(0,0,0,0.15)',
            }}/>
          </button>
        </div>
      </div>
    </div>
  );
}

window.TweaksPanel = TweaksPanel;
