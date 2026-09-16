export default function ExplainabilityBento() {
  return (
    <div className="bento-item col-span-12 row-span-2">
      <h2 className="widget-title">Model Explainability (SHAP Values)</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '16px', fontSize: '0.9rem' }}>
        Global feature importance for XGBoost SLA prediction. Analyzes how Borough, Agency, and Complaint Type impact the delay probability.
      </p>
      <div style={{ width: '100%', display: 'flex', justifyContent: 'center', background: 'rgba(255,255,255,0.02)', borderRadius: 'var(--radius-md)', padding: '16px' }}>
        <img 
          src="/shap_summary.png" 
          alt="SHAP Summary Plot" 
          style={{ maxWidth: '100%', maxHeight: '400px', objectFit: 'contain', borderRadius: '8px' }} 
        />
      </div>
    </div>
  );
}
