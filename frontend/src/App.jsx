import { useRef } from 'react'
import ProjectDocumentationBento from './components/ProjectDocumentationBento'
import SlaPredictorBento from './components/SlaPredictorBento'
import AiAnalystBento from './components/AiAnalystBento'
import ExplainabilityBento from './components/ExplainabilityBento'
import gsap from 'gsap'
import { useGSAP } from '@gsap/react'

gsap.registerPlugin(useGSAP)

function App() {
  const container = useRef()

  useGSAP(() => {
    // Header animation
    gsap.from(".dashboard-header", {
      y: -20,
      opacity: 0,
      duration: 0.6,
      ease: "power2.out"
    })
    
    // Bento boxes stagger animation
    gsap.from(".bento-item", {
      y: 50,
      opacity: 0,
      duration: 0.8,
      stagger: 0.15,
      ease: "power3.out",
      delay: 0.2
    })
  }, { scope: container })

  return (
    <div className="dashboard-container" ref={container}>
      <header className="dashboard-header">
        <h1>CityOps AI</h1>
        <p>Command Center & Analytics</p>
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
