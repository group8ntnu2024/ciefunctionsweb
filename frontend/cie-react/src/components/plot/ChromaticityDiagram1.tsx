import React from 'react';
import Plot from 'react-plotly.js';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';
import { useContentController } from '../../hooks/useContentController';
import { MethodOption, titles } from '../../utils/propTypes';
import { Data } from 'plotly.js';

/*
This diagram layout works for 
  * Maxwellian lm chromaticity diagram
  * CIE xy cone-fundamental-based chromaticity diagram
  * CIE xy standard chromaticity diagram
*/
interface ChromaticityDiagram1 {
  wavelength: number;
  x: number;
  y: number;
}

//TODO: add info
const ChromaticityDiagram1: React.FC = () => {
  const { computedData, isLoading } = useParameters();
  const { selectedOption } = useContentController();

  const plotTitle = (selectedOption && titles[selectedOption as MethodOption]) ? titles[selectedOption as MethodOption] : 'Chromaticity Diagram';


  const xValues = computedData.plotData.map(item => item[1]); 
  const yValues = computedData.plotData.map(item => item[2]);
  const minX = Math.min(...xValues) - 0.1;
  const maxX = Math.max(...xValues) + 0.1;
  const minY = Math.min(...yValues) - 0.1;
  const maxY = Math.max(...yValues) + 0.1;


  const firstPoint = { x: xValues[0], y: yValues[0] };
// Find the southeastern point
const maxIndex = xValues.reduce((maxI, x, i, arr) => x > arr[maxI] ? i : maxI, 0);
const southeasternPoint = computedData.plotData[maxIndex];

  if (!computedData || !computedData.plotData || computedData.plotData.length === 0) {
    return <div>No data available for plotting.</div>;
  }

  if (isLoading) {
    return <LoadingIndicator />;
  }

  // Prepare chart data with all points in a single trace
  const chartData: Data[] = [
    {
    x: xValues,
    y: yValues,
    type: 'scatter',
    mode: 'lines',
    marker: {
      color: 'black', // Set line color to black
      width: 2 // Set line width to make it thinner
    }
    },
    {
      x: [firstPoint.x, southeasternPoint[1]], // x values from the first and southeastern points
      y: [firstPoint.y, southeasternPoint[2]], // y values from the first and southeastern points
      type: 'scatter',
      mode: 'lines',
      line: {
        color: 'red',
        width: 2
      }
    
  }];

  try {
    return (
      <Plot
        data={chartData}
        layout={{
          width: 800,
          height: 600,
          title: plotTitle,
          xaxis: {
            title: 'Chromaticity x',
            range: [minX, maxX]  // Set the range with added buffer
          },
          yaxis: {
            title: 'Chromaticity y',
            range: [minY, maxY]  // Set the range with added buffer
          },
          autosize: false,
          margin: { l: 50, r: 10, b: 50, t: 50, pad: 4 },
          showlegend: false
        }}
        config={{
          scrollZoom: true,
          displaylogo: false
        }}
      />
    );
  } catch (error) {
    console.error("Error rendering plot:", error);
    return <div>Error displaying plot. Please check the console for more details.</div>;
  }
};

export default ChromaticityDiagram1;