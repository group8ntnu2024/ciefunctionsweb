import React from 'react';
import Plot from 'react-plotly.js';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';
import { useContentController } from '../../hooks/useContentController';
import { MethodOption, titles } from '../../utils/propTypes';
import { Data } from 'plotly.js';


/*
This diagram layout works for 
  * xy cone-fundamental-based chromaticity diagram (purple-line stimuli)
*/

const XyConeFundamentalBasedChromaticityDiagramPls: React.FC = () => {
  const { computedData, isLoading } = useParameters();
  const { selectedOption } = useContentController();

  const plotTitle = (selectedOption && titles[selectedOption as MethodOption]) ? titles[selectedOption as MethodOption] : 'Chromaticity Diagram';

  if (!computedData || !computedData.plotData || computedData.plotData.length === 0) {
    return <div>No data available for plotting.</div>;
  }

  if (isLoading) {
    return <LoadingIndicator />;
  }

  function addSpecificWavelengthPoints() {
    const startWavelength = 400;
    const endWavelength = 700;
    const step = 10;
    const additionalWavelengths = [390,407.3];
    //drawnPoints.push(0);
    //drawnPoints.push(computedData.plotData.length - 1);

    for (let wavelength = startWavelength; wavelength <= endWavelength; wavelength += step) {
        const index = wavelengths.indexOf(wavelength);
        if (index !== -1) {
            drawnPoints.push(index);
        }
    }

    additionalWavelengths.forEach(wavelength => {
        const index = wavelengths.indexOf(wavelength);
        if (index !== -1) {
            drawnPoints.push(index);
        }
    });
}

  const purpleXValues = computedData.plotData.map(item => item[1]); 
  const purpleYValues = computedData.plotData.map(item => item[2]);
  const wavelengths = computedData.plotData.map(item => item[0]);

  const drawnPoints: number[] = [];
  addSpecificWavelengthPoints();


  // Extracting purple line points if available and adding it to the plot
  const chartData: Data[] = [
    {
      x: purpleXValues,
      y: purpleYValues,
      type: 'scatter',
      mode: 'lines',
      line: {
        color: 'black',
        width: 2
      }
    }
  ];

  // Extends the purple line fully
  if (computedData.purpleLineData) {  
    const xValues = computedData.purpleLineData.map(item => item[1]);
    const yValues = computedData.purpleLineData.map(item => item[2]);

      chartData.push({
        x: xValues,
        y: yValues,
        type: 'scatter',
        mode: 'lines',
        line: {
          color: 'black',
          width: 2
        }
      });
  }

  // first and last poins for purple line
  if (computedData.purpleLineData && computedData.purpleLineData.length > 1) {
    // Safely access the first and last points
    const firstPoint = computedData.purpleLineData[0];
    const lastPoint = computedData.purpleLineData[computedData.purpleLineData.length - 1];
  
    if (firstPoint && lastPoint && firstPoint.length > 2 && lastPoint.length > 2) {
      chartData.push({
        x: [firstPoint[1], lastPoint[1]],
        y: [firstPoint[2], lastPoint[2]],
        type: 'scatter',
        mode: 'markers',
        marker: {
          color: 'white',
          size: 10,
          line: {
            color: 'black',
            width: 2
          },
          symbol: 'circle'
        }
      });
    } else {
      console.error("Error: Data points are not structured as expected.");
    }
  } else {
    console.error("Error: 'purpleLineData' is not loaded or does not contain enough data.");
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


  // Draws circles on the
  drawnPoints.forEach(index => {
    chartData.push({
      x: [purpleXValues[index]],
      y: [purpleYValues[index]],
      type: 'scatter',
      mode: 'markers',
      marker: {
        color: 'white',
        size: 10,
        line: {
          color: 'black',
          width: 2
        },
        symbol: 'circle'
      }
    });
  });
  
    // Prepares plot data with in the arch of the chromaticity diagram and sets up the plot
  if (computedData.plsArchData) {
    const xValues = computedData.plsArchData.map(item => item[1]);
    const yValues = computedData.plsArchData.map(item => item[2]);

    const minX = Math.min(...xValues) - 0.1;
    const maxX = Math.max(...xValues) + 0.1;
    const minY = Math.min(...yValues) - 0.1;
    const maxY = Math.max(...yValues) + 0.1;

    chartData.push({
        x: xValues,
        y: yValues,
        type: 'scatter',
        mode: 'lines',
        line: {
            color: 'black',
            width: 2
        }
    });

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
        return <div>Error displaying plot.</div>;
    }
} else {
    console.error("Error: 'plsArchData' is not loaded or does not contain enough data.");
}
};
export default XyConeFundamentalBasedChromaticityDiagramPls;