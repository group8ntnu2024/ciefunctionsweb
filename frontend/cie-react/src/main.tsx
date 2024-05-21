import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

/**
 * Entry point for the React application.
 * Renders App component into root element of the HTML document
 * 
 * React.StrictMode is used to highlight potential problems
 * troughout the application.
 */
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
