import { useState } from 'react'
import './App.css'

function App() {
  const [cliques, setCliques] = useState(0)

  return (
    <div className="container">
      <h1>Página de Cliques</h1>
      
      <p>Você clicou no botão <strong>{cliques}</strong> vezes.</p>
      
      <button 
        className="botao-contador"
        onClick={() => setCliques(cliques + 1)}
      >
        Clique-me
      </button>
    </div>
  )
}

export default App