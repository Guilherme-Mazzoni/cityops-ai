import { useState, useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

export default function SlaPredictorBento() {
  const [formData, setFormData] = useState({ borough: 'BROOKLYN', agency: 'NYPD', complaint_type: 'Noise' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  
  const container = useRef();
  const gaugeRef = useRef();
  const textRef = useRef();

  useGSAP(() => {
    if (result !== null && gaugeRef.current && textRef.current) {
      gsap.fromTo(textRef.current, 
        { innerHTML: 0 }, 
        { 
          innerHTML: result, 
          duration: 1.2, 
          snap: { innerHTML: 1 }, 
          ease: "power2.out",
          onUpdate: function() {
            textRef.current.innerHTML = Math.round(this.targets()[0].innerHTML) + '%';
          }
        }
      );
      
      let severityColor = "#429e47"; // Green
      if (result >= 40 && result < 75) severityColor = "#e5a329"; // Yellow/Orange
      if (result >= 75) severityColor = "#d64e4e"; // Red
      
      gsap.fromTo(gaugeRef.current,
        { "--gauge-value": "0%" },
        { "--gauge-value": `${result}%`, "--gauge-color": severityColor, duration: 1.2, ease: "power2.out" }
      );
      
      gsap.from(".prediction-result > *", {
        opacity: 0,
        duration: 0.4,
        stagger: 0.1,
        ease: "power1.out"
      });
    }
  }, { dependencies: [result], scope: container });

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch(`${API_URL}/predict-sla`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (data.error) {
        setErrorMsg(data.error);
        setResult(null);
      } else {
        setResult(data.probability ? Math.round(data.probability * 100) : 0);
      }
    } catch (error) {
      console.error(error);
      setErrorMsg("Erro de Conexão: Servidor API (FastAPI) está offline.");
      setResult(null);
    }
    setLoading(false);
  };

  return (
    <div className="bento-item col-span-4" ref={container} style={{ display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
      <h2 className="widget-title">Preditor de SLA</h2>
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: result !== null ? '24px' : 'auto' }}>
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label className="form-label">Distrito</label>
          <select className="form-select" value={formData.borough} onChange={e => setFormData({...formData, borough: e.target.value})}>
            <option value="BROOKLYN">Brooklyn</option>
            <option value="QUEENS">Queens</option>
            <option value="MANHATTAN">Manhattan</option>
            <option value="BRONX">Bronx</option>
            <option value="STATEN ISLAND">Staten Island</option>
          </select>
        </div>
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label className="form-label">Agência Responsável</label>
          <select className="form-select" value={formData.agency} onChange={e => setFormData({...formData, agency: e.target.value})}>
            <option value="NYPD">NYPD</option>
            <option value="DSNY">DSNY</option>
            <option value="DEP">DEP</option>
            <option value="DOT">DOT</option>
          </select>
        </div>
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label className="form-label">Tipo de Reclamação</label>
          <input className="form-input" type="text" placeholder="Ex: Noise..." value={formData.complaint_type} onChange={e => setFormData({...formData, complaint_type: e.target.value})} />
        </div>
        
        {errorMsg && (
          <div style={{ color: '#DC2626', fontSize: '0.85rem', padding: '8px', background: '#FEE2E2', borderRadius: '4px' }}>
            {errorMsg}
          </div>
        )}

        <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: '8px' }}>
          {loading ? 'Processando...' : 'Calcular Previsão'}
        </button>
      </form>

      {result !== null && (
        <div className="prediction-result" style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid var(--surface-border)' }}>
          <div className="gauge-container" ref={gaugeRef} style={{ '--gauge-value': `${result}%`, margin: '0 auto 8px auto', width: '100px', height: '100px' }}>
            <div className="gauge-inner" ref={textRef} style={{ width: '84px', height: '84px', fontSize: '1.2rem' }}>{result}%</div>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: 0 }}>Probabilidade de Atraso</p>
        </div>
      )}
    </div>
  );
}
