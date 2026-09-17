export default function ExplainabilityBento() {
  return (
    <div className="bento-item col-span-12 row-span-2">
      <h2 className="widget-title">Entendendo a Decisão da IA (Valores SHAP)</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '16px', fontSize: '0.9rem' }}>
        Importância global das variáveis no modelo preditivo (XGBoost). Analisa como o Distrito, a Agência e o Tipo de Reclamação impactam o atraso matematicamente.
      </p>
      <div style={{ width: '100%', display: 'flex', justifyContent: 'center', background: '#F9FAFB', border: '1px solid #E5E7EB', borderRadius: 'var(--radius-md)', padding: '16px' }}>
        <img 
          src="/shap_summary.png" 
          alt="Gráfico de Valores SHAP" 
          style={{ maxWidth: '100%', maxHeight: '400px', objectFit: 'contain', borderRadius: '8px' }} 
        />
      </div>
    </div>
  );
}
