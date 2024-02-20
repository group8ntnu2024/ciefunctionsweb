import { useState } from 'react';
import './App.css';
import FetchedChart from './components/chart';
import FetchedTable from './components/table';

function App() {
  const [activeTab, setActiveTab] = useState('Plot');

  return (
    <div className="App">
      <div className="tabs">
        <button
          className={`tab-button ${activeTab === 'Plot' ? 'active' : ''}`}
          onClick={() => setActiveTab('Plot')}
        >
          Plot
        </button>
        <button
          className={`tab-button ${activeTab === 'Table' ? 'active' : ''}`}
          onClick={() => setActiveTab('Table')}
        >
          Table
        </button>
      </div>
      <div className="content-container">
        {activeTab === 'Plot' && <FetchedChart />}
        {activeTab === 'Table' && <FetchedTable />}
      </div>
    </div>
  );
}

export default App;
