export default function ExplainabilityBento() {
  return (
    <div className="bento-item col-span-5" style={{ display: 'flex', flexDirection: 'column' }}>
      <h2 className="widget-title">Entendendo a Decisão da IA (Valores SHAP)</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '16px', fontSize: '0.9rem' }}>
        Importância global das variáveis no modelo preditivo (XGBoost). Analisa como o Distrito, a Agência e o Tipo de Reclamação impactam o atraso matematicamente.
      </p>
      <div style={{ width: '100%', height: '280px', display: 'flex', justifyContent: 'center', alignItems: 'center', background: '#e2e8f0', border: '1px solid var(--surface-border)', padding: '8px', overflow: 'hidden', borderRadius: 'var(--radius-md)' }}>
        <img 
          src="/shap_summary.png" 
          alt="Gráfico de Valores SHAP" 
          style={{ width: '100%', height: '100%', objectFit: 'contain', mixBlendMode: 'multiply' }} 
        />
      </div>
    </div>
  );
}
