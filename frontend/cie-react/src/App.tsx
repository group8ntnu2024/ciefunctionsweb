//import { useState, useEffect } from 'react';
import './App.css'
import FetchedChart from './components/chart'
import FetchedTable from './components/table';

function App() {
  return (
    <div className="App">
      <div className="chart-container">
        <FetchedChart />
      </div>
      <div className="table-container">
        <FetchedTable />
      </div>
    </div>
  );
}

export default App;
