import React from 'react';
import Plot from 'react-plotly.js';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';
import { useContentController } from '../../hooks/useContentController';
import { MethodOption, titles } from '../../utils/propTypes';
import { Data } from 'plotly.js';


/*
This diagram layout works for 
  * MacLeod–Boynton ls chromaticity diagram
*/

interface ChromaticityDiagram2 {
  wavelength: number;
  x: number;
  y: number;
}

const ChromaticityDiagram2: React.FC = () => {
  const { computedData, isLoading } = useParameters();
  const { selectedOption } = useContentController();

  const plotTitle = (selectedOption && titles[selectedOption as MethodOption]) ? titles[selectedOption as MethodOption] : 'Chromaticity Diagram';


  const xValues = computedData.plotData.map(item => item[1]); 
  const yValues = computedData.plotData.map(item => item[3]);

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
        color: 'black', // Assuming intensity of 0.8 for illustration; adjust as needed
        size: 2
      }
    }
  ];

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
            range: [-0.05, 1.05] // Set x-axis range
          },
          yaxis: {
            title: 'Chromaticity y',
            range: [-0.05, 1.05] // Set y-axis range
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

export default ChromaticityDiagram2;