import ProjectDocumentationBento from './components/ProjectDocumentationBento'
import SlaPredictorBento from './components/SlaPredictorBento'
import AiAnalystBento from './components/AiAnalystBento'
import ExplainabilityBento from './components/ExplainabilityBento'

function App() {
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>CityOps AI</h1>
        <p>Plataforma de Analytics e Gestão Pública</p>
      </header>
      
      <main className="bento-grid">
        <ProjectDocumentationBento />
        <SlaPredictorBento />
        <AiAnalystBento />
        <ExplainabilityBento />
      </main>
    </div>
  )
}

export default App
