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
          duration: 2, 
          snap: { innerHTML: 1 }, 
          ease: "power3.out",
          onUpdate: function() {
            textRef.current.innerHTML = Math.round(this.targets()[0].innerHTML) + '%';
          }
        }
      );
      
      gsap.fromTo(gaugeRef.current,
        { "--gauge-value": "0%" },
        { "--gauge-value": `${result}%`, duration: 2, ease: "power3.out" }
      );
      
      gsap.from(".prediction-result > *", {
        y: 20,
        opacity: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: "power2.out"
      });
    }
  }, { dependencies: [result], scope: container });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch('http://localhost:8000/predict-sla', {
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
    <div className="bento-item col-span-4" ref={container}>
      <h2 className="widget-title">Preditor de SLA</h2>
      
      {result !== null ? (
        <div className="prediction-result">
          <div className="gauge-container" ref={gaugeRef} style={{ '--gauge-value': `${result}%` }}>
            <div className="gauge-inner" ref={textRef}>{result}%</div>
          </div>
          <p style={{ color: 'var(--text-secondary)' }}>Probabilidade de Atraso</p>
          <button className="btn-primary" style={{ marginTop: '32px' }} onClick={() => setResult(null)}>
            Nova Análise
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
          <div className="form-group">
            <label className="form-label">Distrito</label>
            <select className="form-select" value={formData.borough} onChange={e => setFormData({...formData, borough: e.target.value})}>
              <option value="BROOKLYN">Brooklyn</option>
              <option value="QUEENS">Queens</option>
              <option value="MANHATTAN">Manhattan</option>
              <option value="BRONX">Bronx</option>
              <option value="STATEN ISLAND">Staten Island</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Agência Responsável</label>
            <select className="form-select" value={formData.agency} onChange={e => setFormData({...formData, agency: e.target.value})}>
              <option value="NYPD">NYPD</option>
              <option value="DSNY">DSNY</option>
              <option value="DEP">DEP</option>
              <option value="DOT">DOT</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Tipo de Reclamação</label>
            <input className="form-input" type="text" placeholder="Ex: Noise, Rodents..." value={formData.complaint_type} onChange={e => setFormData({...formData, complaint_type: e.target.value})} />
          </div>
          
          {errorMsg && (
            <div style={{ color: '#DC2626', fontSize: '0.85rem', marginBottom: '16px', padding: '8px', background: '#FEE2E2', borderRadius: '4px' }}>
              {errorMsg}
            </div>
          )}

          <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: 'auto' }}>
            {loading ? 'Processando...' : 'Calcular Previsão'}
          </button>
        </form>
      )}
    </div>
  );
}
