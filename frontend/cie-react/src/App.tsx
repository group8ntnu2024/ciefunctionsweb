import { useState } from 'react';
import './App.css';
import FetchedChart from './components/chart';
import FetchedTable from './components/table';

function App() {
  const [activeTab, setActiveTab] = useState('Plot');
  const [selectedLibrary, setSelectedLibrary] = useState('Recharts');

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
        {activeTab === 'Plot' && (
          <>
            <div className="chart-selection">
              <label htmlFor="chart-library">Select plot library: </label>
              <select
                id="chart-library"
                value={selectedLibrary}
                onChange={(event) => setSelectedLibrary(event.target.value)}
              >
                <option value="Recharts">Recharts</option>
                <option value="Chartjs">Plot Lib 2</option>
              </select>
            </div>
            {selectedLibrary === 'Recharts' ? (
              <FetchedChart />
            ) : (
              <div className='centered-content'>Plot 2 will show here</div>
            )}
          </>
        )}
        {activeTab === 'Table' && <FetchedTable />}
      </div>
    </div>
  );
}

export default App;
