import { useState } from 'react';

export default function ExplainabilityBento() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <div className="bento-item col-span-5">
        <h2 className="widget-title">Entendendo a Decisão da IA (Valores SHAP)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '16px', fontSize: '0.9rem' }}>
          Importância global das variáveis no modelo preditivo (XGBoost). Analisa como o Distrito, a Agência e o Tipo de Reclamação impactam o atraso matematicamente.
        </p>
        <div style={{ width: '100%', height: '350px', display: 'flex', justifyContent: 'center', alignItems: 'center', background: '#e2e8f0', border: '1px solid var(--surface-border)', padding: '8px', overflow: 'hidden', borderRadius: 'var(--radius-md)' }}>
          <img 
            src="/shap_summary.png" 
            alt="Gráfico de Valores SHAP" 
            onClick={() => setIsModalOpen(true)}
            style={{ width: '100%', height: '100%', objectFit: 'contain', mixBlendMode: 'multiply', cursor: 'zoom-in', transition: 'transform 0.2s ease' }} 
            onMouseOver={e => e.currentTarget.style.transform = 'scale(1.02)'}
            onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
          />
        </div>
      </div>

      {isModalOpen && (
        <div 
          style={{
            position: 'fixed',
            top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            zIndex: 9999,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            cursor: 'zoom-out',
            padding: '24px'
          }}
          onClick={() => setIsModalOpen(false)}
        >
          <img 
            src="/shap_summary.png" 
            alt="Gráfico de Valores SHAP em Tela Cheia" 
            style={{
              maxWidth: '100%',
              maxHeight: '100%',
              objectFit: 'contain',
              background: '#fff', /* Background for transparent PNGs so they are visible */
              borderRadius: '8px',
              boxShadow: '0 10px 40px rgba(0,0,0,0.5)'
            }} 
          />
        </div>
      )}
    </>
  );
}
