import React from 'react';
import Plot from 'react-plotly.js';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';
import { useContentController } from '../../hooks/useContentController';
import { MethodOption, titles } from '../../utils/propTypes';
import { Data } from 'plotly.js';

const XyConeFundamentalBasedChromaticityDiagram: React.FC = () => {
  const { computedData, isLoading } = useParameters();
  const { selectedOption } = useContentController();

  const plotTitle = (selectedOption && titles[selectedOption as MethodOption]) ? titles[selectedOption as MethodOption] : 'Chromaticity Diagram';

  if (!computedData || !computedData.plotData || computedData.plotData.length === 0) {
    return <div>No data available for plotting.</div>;
  }

  if (isLoading) {
    return <LoadingIndicator />;
  }

  const xValues = computedData.plotData.map(item => item[1]); 
  const yValues = computedData.plotData.map(item => item[2]);

  // Prepares plot data with in the arch of the chromaticity diagram
  const chartData: Data[] = [
    {
      x: xValues,
      y: yValues,
      type: 'scatter',
      mode: 'lines',
      line: {
        color: 'black',
        width: 2
      }
    }
  ];

  // Extracting purple line points if available and adding it to the plot
  if (computedData.purpleLineData) {
    const purpleXValues = computedData.purpleLineData.map(item => item[1]);
    const purpleYValues = computedData.purpleLineData.map(item => item[2]);

    chartData.push({
      x: purpleXValues,
      y: purpleYValues,
      type: 'scatter',
      mode: 'lines',
      line: {
        color: 'black',
        width: 2
      }
    });
  }

  // Adding the white point if available
  if (computedData.whitePointData) {
    const whiteX = [computedData.whitePointData[0]];
    const whiteY = [computedData.whitePointData[2]];

    chartData.push({
      x: whiteX,
      y: whiteY,
      type: 'scatter',
      mode: 'markers',
      marker: {
        color: 'red',
        symbol: 'x-thin',
        size: 10,
        line: {
          color: 'black',
          width: 1
        }
      }
    });
  }

  const minX = Math.min(...xValues) - 0.1;
  const maxX = Math.max(...xValues) + 0.1;
  const minY = Math.min(...yValues) - 0.1;
  const maxY = Math.max(...yValues) + 0.1;

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
            range: [minX, maxX]
          },
          yaxis: {
            title: 'Chromaticity y',
            range: [minY, maxY]
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

export default XyConeFundamentalBasedChromaticityDiagram;
