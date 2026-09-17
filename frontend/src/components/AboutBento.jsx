export default function AboutBento() {
  return (
    <div className="bento-item col-span-12">
      <h2 className="widget-title">Sobre o CityOps AI</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', marginTop: '16px' }}>
        
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px' }}>🎯 O Problema</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            A Prefeitura de Nova York recebe milhões de chamados via 311 (Buracos, Lixo, Ruído). Muitos desses chamados sofrem **atrasos críticos** (quebra de SLA), custando tempo e dinheiro público por falta de triagem inteligente.
          </p>
        </div>

        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px' }}>🚀 A Solução (Este Dashboard)</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Criamos uma plataforma preditiva. O **XGBoost** lê o Distrito e Agência e prevê matematicamente a chance de atraso antes mesmo de acontecer. Além disso, um sistema de **IA Generativa RAG (Qwen 2.5)** atua como um analista autônomo, minerando os dados reais.
          </p>
        </div>

        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px' }}>💡 Como Avaliar (Guia)</h3>
          <ul style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6, paddingLeft: '20px' }}>
            <li>Troque o Distrito para <strong>QUEENS</strong> e a agência para <strong>DEP</strong> e observe a probabilidade de SLA recalcular em tempo real.</li>
            <li>Digite <em>"Quais bairros têm mais chamados?"</em> no Analista IA e veja o RAG buscar do banco de dados vetorial.</li>
          </ul>
        </div>
        
      </div>
    </div>
  );
}
