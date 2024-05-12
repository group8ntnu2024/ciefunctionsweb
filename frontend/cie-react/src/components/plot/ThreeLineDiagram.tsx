import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';
import { useContentController } from '../../hooks/useContentController';
import { MethodOption, titles } from '../../utils/propTypes';
import './props.css';

type ThreeLineDiagram = {
  x: number[];
  y: number[];
  type: 'scatter';
  mode: 'lines' | 'markers';
  name: string;
  marker: { color: string };
}[];

const ThreeLineDiagram: React.FC = () => {
  const { computedData, isLoading } = useParameters();
  const { selectedOption } = useContentController();
  const [showGrid, setShowGrid] = useState(true);

  const plotTitle = (selectedOption in titles) ? titles[selectedOption as MethodOption] : 'Select a method';

  const xValues = computedData.plotData.map(item => item[0]); 
  const y1Values = computedData.plotData.map(item => item[1]);
  const y2Values = computedData.plotData.map(item => item[2]);
  const y3Values = computedData.plotData.map(item => item[3]);

  const chartData: ThreeLineDiagram = [
    {
      x: xValues, 
      y: y1Values,
      type: 'scatter',
      mode: 'lines',
      name: 'Y1',
      marker: { color: 'red' },
    },
    {
      x: xValues, 
      y: y2Values,
      type: 'scatter',
      mode: 'lines',
      name: 'Y2',
      marker: { color: 'green' },
    },
    {
      x: xValues,
      y: y3Values,
      type: 'scatter',
      mode: 'lines',
      name: 'Y3',
      marker: { color: 'blue' },
    },
  ];

  if (isLoading) {
    return <LoadingIndicator />;
  }

  return (
    <div>
      <Plot
        data={chartData}
        layout={{
          width: 800,
          height: 600,
          title: plotTitle,
          margin: { l: 85, r: 10, b: 60, t: 75, pad: 4 },
          xaxis: { 
            title: 'Wavelength (nm)',
            showgrid: showGrid,
            gridcolor: 'rgba(0, 0, 0, 0.3)',
            showline: true,
            linecolor: 'black',
            linewidth: 2,
            mirror: true
          },
          yaxis: { 
            title: 'Relative energy sensitivities',
            showgrid: showGrid,
            gridcolor: 'rgba(0, 0, 0, 0.3)',
            showline: true,
            linecolor: 'black',
            linewidth: 2,
            mirror: true
          },
        }}
        config={{
          scrollZoom: true,
          displaylogo: false
        }}
      />
      <div className="checkbox-container">
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={showGrid}
            onChange={() => setShowGrid(!showGrid)}
          />
          Show Grid
        </label>
      </div>
    </div>
  );
};

export default ThreeLineDiagram;
