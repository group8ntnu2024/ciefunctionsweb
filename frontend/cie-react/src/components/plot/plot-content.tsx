import { useState } from 'react';
import '../app-content.css';
import RechartPlot from './rechart-plot';
import PlotlyPlot from './plotly-plot';

function PlotContent() {
  const [selectedLibrary, setSelectedLibrary] = useState('Recharts');

  return (
      <div className="content-container">
          <>
            <div className="chart-selection">
              <label htmlFor="chart-library">Select plot library: </label>
              <select
                id="chart-library"
                value={selectedLibrary}
                onChange={(event) => setSelectedLibrary(event.target.value)}
              >
                <option value="Recharts">Recharts</option>
                <option value="Plotly">Plotly</option>
              </select>
            </div>
            {selectedLibrary === 'Recharts' ? (
              <RechartPlot />

            ) : selectedLibrary === 'Plotly' ? (
              <PlotlyPlot/>
            ) : ( 
              <div className='centered-content'>Plot 2 will show here</div>
            )}
            
          </>
      </div> 
  );
}

export default PlotContent;
