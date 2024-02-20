import { useState } from 'react'
import dodoLogo from './assets/dodo.png'
import './App.css'

function App() {
  //count used for button presses
  const [count, setCount] = useState(0)
  
  //Parameters for spinning image
  const [spinDirection, setSpinDirection] = useState('spin-clockwise')
  const toggleSpinDirection = () => {
    setSpinDirection((prevDirection) =>
      prevDirection === 'spin-clockwise' ? 'spin-counterclockwise' : 'spin-clockwise'
    );
  };

  return (
    <>
      <div>
      <img src={dodoLogo} className={`logo ${spinDirection}`} alt="logo" onClick={toggleSpinDirection} />
      </div>
      <h1>Hello World!</h1>
      <p>Number of times clicked: {count }</p>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          Button
        </button>
      </div>
      <button onClick={() => setCount(() => 0)}>
          Reset count
        </button>
    </>
  )
}

export default App