import SlaPredictorBento from './components/SlaPredictorBento'
import AiAnalystBento from './components/AiAnalystBento'

function App() {
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>CityOps Intelligence</h1>
        <p>Advanced Urban Analytics Platform</p>
      </header>
      
      <main className="bento-grid">
        <SlaPredictorBento />
        <AiAnalystBento />
      </main>
    </div>
  )
}

export default App
