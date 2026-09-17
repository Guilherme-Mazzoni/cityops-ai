import { useState } from 'react';

export default function ProjectDocumentationBento() {
  const [activeTab, setActiveTab] = useState('business');

  return (
    <div className="bento-item col-span-8">
      <h2 className="widget-title">CityOps AI: Architecture & Business Value</h2>
      
      <div className="tabs-header">
        <button className={`tab-btn ${activeTab === 'business' ? 'active' : ''}`} onClick={() => setActiveTab('business')}>🏢 Visão de Negócios</button>
        <button className={`tab-btn ${activeTab === 'architecture' ? 'active' : ''}`} onClick={() => setActiveTab('architecture')}>⚙️ Eng. de Dados & Arquitetura</button>
        <button className={`tab-btn ${activeTab === 'ml' ? 'active' : ''}`} onClick={() => setActiveTab('ml')}>🧠 Machine Learning</button>
        <button className={`tab-btn ${activeTab === 'rag' ? 'active' : ''}`} onClick={() => setActiveTab('rag')}>🤖 GenAI & RAG</button>
      </div>

      <div className="tab-content" style={{ minHeight: '180px' }}>
        
        {activeTab === 'business' && (
          <div className="tab-content-pane">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>O Impacto Financeiro dos SLAs</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '12px' }}>
              Metrópoles como Nova York processam milhões de chamados pelo canal 311 (Lixo, Ruído, Buracos). Quando uma agência falha em cumprir o prazo acordado (SLA), a prefeitura sofre com multas, desperdício de recursos e insatisfação pública. 
            </p>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6 }}>
              <strong>Nossa Solução:</strong> Ao invés de agir de forma reativa, o <em>CityOps AI</em> aplica Machine Learning para atuar na <strong>Triagem Preditiva</strong>. Ao saber matematicamente quais chamados têm mais de 70% de chance de atrasar antes mesmo de despachar a equipe, gestores podem priorizar rotas e alocar recursos preventivamente, economizando milhões em processos ineficientes.
            </p>
          </div>
        )}

        {activeTab === 'architecture' && (
          <div className="tab-content-pane">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>Modern Data Stack</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '12px' }}>
              Este projeto consolida as melhores práticas de Engenharia de Software e Dados da atualidade. 
            </p>
            <ul style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, paddingLeft: '20px' }}>
              <li><strong>Transformação de Dados (ELT):</strong> Usamos <code>dbt</code> (Data Build Tool) acoplado a um banco de dados PostgreSQL para limpar os dados brutos de NYC, calcular tempos de resolução históricos e tipificar métricas analíticas (`mart_sla`).</li>
              <li><strong>Backend (FastAPI):</strong> Uma API assíncrona extremamente veloz em Python, responsável por orquestrar tanto a inferência do modelo XGBoost quanto as rotas de IA Generativa.</li>
              <li><strong>Frontend (React + Vite):</strong> Single-Page Application estruturada no padrão <em>Bento Grid</em>, sem depender de frameworks visuais pesados, garantindo performance e escalabilidade.</li>
            </ul>
          </div>
        )}

        {activeTab === 'ml' && (
          <div className="tab-content-pane">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>XGBoost & MLflow (MLOps)</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '12px' }}>
              No lugar de heurísticas simples, optamos pelo <strong>XGBoost</strong>, um poderoso algoritmo de <em>Gradient Boosting</em>, ideal para lidar com dados tabulares complexos e não lineares da prefeitura.
            </p>
            <ul style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, paddingLeft: '20px' }}>
              <li><strong>Feature Engineering:</strong> As variáveis categóricas (Distrito, Agência, Tipo) são mapeadas em matrizes esparsas gigantes via <code>One-Hot Encoding</code>.</li>
              <li><strong>Versionamento de Modelos:</strong> Todo o treinamento é rastreado via <code>MLflow</code>. Isso nos permite comparar métricas (F1-Score, ROC-AUC) entre diferentes algoritmos. O Frontend não "chuta" um valor: a API consome o artefato real empacotado pelo MLflow.</li>
              <li><strong>Explicabilidade (XAI):</strong> Utilizamos a biblioteca <code>SHAP</code> (abaixo) para abrir a "caixa preta" e provar para as partes interessadas (Stakeholders) quais variáveis causam os atrasos.</li>
            </ul>
          </div>
        )}

        {activeTab === 'rag' && (
          <div className="tab-content-pane">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '12px' }}>Retrieval-Augmented Generation (RAG)</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '12px' }}>
              Para dar autonomia analítica a gestores que não sabem programar SQL, construímos um chat equipado com IA Generativa, porém 100% ancorado (grounded) nos dados do banco, eliminando alucinações.
            </p>
            <ul style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, paddingLeft: '20px' }}>
              <li><strong>Embeddings:</strong> Usamos o <code>sentence-transformers</code> (HuggingFace) para converter milhares de linhas de chamados em matrizes matemáticas de 384 dimensões.</li>
              <li><strong>Busca Vetorial:</strong> Estas matrizes são salvas no PostgreSQL usando a extensão <code>pgvector</code>. Quando o usuário faz uma pergunta, o sistema realiza uma busca de similaridade de cosseno (Cosine Similarity) para achar as 5 reclamações históricas mais parecidas com o contexto.</li>
              <li><strong>LLM de Borda:</strong> Passamos esse contexto ultra-preciso para o modelo Open Source <code>Qwen 2.5</code> (via API da Groq), que atua apenas como um "intérprete" dos fatos.</li>
            </ul>
          </div>
        )}

      </div>
    </div>
  );
}
