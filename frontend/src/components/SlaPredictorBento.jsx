import { useState } from 'react';

export default function SlaPredictorBento() {
  const [formData, setFormData] = useState({ borough: 'BROOKLYN', agency: 'NYPD', complaint_type: 'Noise' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/predict-sla', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      setResult(data.probability ? Math.round(data.probability * 100) : 0);
    } catch (error) {
      console.error(error);
      setResult(0);
    }
    setLoading(false);
  };

  return (
    <div className="bento-item col-span-4">
      <h2 className="widget-title">Predictive SLA Analysis</h2>
      
      {result !== null ? (
        <div className="prediction-result">
          <div className="gauge-container" style={{ '--gauge-value': `${result}%` }}>
            <div className="gauge-inner">{result}%</div>
          </div>
          <p style={{ color: 'var(--text-secondary)' }}>Delay Probability</p>
          <button className="btn-primary" style={{ marginTop: '32px' }} onClick={() => setResult(null)}>
            Run New Analysis
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
          <div className="form-group">
            <label className="form-label">Borough</label>
            <select className="form-select" value={formData.borough} onChange={e => setFormData({...formData, borough: e.target.value})}>
              <option value="BROOKLYN">Brooklyn</option>
              <option value="QUEENS">Queens</option>
              <option value="MANHATTAN">Manhattan</option>
              <option value="BRONX">Bronx</option>
              <option value="STATEN ISLAND">Staten Island</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Agency</label>
            <select className="form-select" value={formData.agency} onChange={e => setFormData({...formData, agency: e.target.value})}>
              <option value="NYPD">NYPD</option>
              <option value="DSNY">DSNY</option>
              <option value="DEP">DEP</option>
              <option value="DOT">DOT</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Complaint Type</label>
            <input className="form-input" type="text" value={formData.complaint_type} onChange={e => setFormData({...formData, complaint_type: e.target.value})} />
          </div>
          <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: 'auto' }}>
            {loading ? 'Processing Model...' : 'Execute Model'}
          </button>
        </form>
      )}
    </div>
  );
}
