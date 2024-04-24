import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';
import { useContentController } from '../../hooks/useContentController';
import { MethodOption, titles } from '../../utils/propTypes';
import { Data } from 'plotly.js';

const XyConeFundamentalBasedChromaticityDiagramPls: React.FC = () => {
  // Fetches data and state from custom hooks
  const { computedData, isLoading } = useParameters();
  const { selectedOption } = useContentController();
  
  // State variables for controlling grid and labels display
  const [showGrid, setShowGrid] = useState(true);
  const [showLabels, setShowLabels] = useState(false);

  // Determines plot title based on selected option
  const plotTitle = (selectedOption && titles[selectedOption as MethodOption]) ? titles[selectedOption as MethodOption] : 'Chromaticity Diagram';

  // Checks if data is available or loading
  if (!computedData || !computedData.plotData || computedData.plotData.length === 0) {
    return <div>No data available for plotting.</div>;
  }

  if (isLoading) {
    return <LoadingIndicator />;
  }

  // Function to add specific wavelength points
  function addSpecificWavelengthPoints() {
    const startWavelength = 400;
    const endWavelength = 700;
    const step = 10;
    const additionalWavelengths = [390, 407.3];

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

  // Extracts data for plotting
  const purpleXValues = computedData.plotData.map(item => item[1]); 
  const purpleYValues = computedData.plotData.map(item => item[2]);
  const wavelengths = computedData.plotData.map(item => item[0]);
  const drawnPoints: number[] = [];
  addSpecificWavelengthPoints();

  // Initial chart data with purple line
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

  // Adds purple line data if available
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

  // Adds markers for purple line first and last point
  if (computedData.purpleLineData && computedData.purpleLineData.length > 1) {
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
  
      // Adding labels if showLabels is true
      if (showLabels) {
        chartData.push({
          x: [firstPoint[1], lastPoint[1]],
          y: [firstPoint[2], lastPoint[2]],
          type: 'scatter',
          mode: 'text',
          text: [`${firstPoint[0]}`, `${lastPoint[0]}`],
          textposition: 'bottom right',
          textfont: {
            color: 'black',
            size: 12
          }
        });
      }
    } else {
      console.error("Error: Data points are not structured as expected.");
    }
  } else {
    console.error("Error: 'purpleLineData' is not loaded or does not contain enough data.");
  }

  // Adds white point marker and label if available
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

    if (showLabels) {
      chartData.push({
        x: whiteX,
        y: whiteY,
        type: 'scatter',
        mode: 'text',
        text: ['T'],
        textposition: 'top right',
        textfont: {
          color: 'black',
          size: 16
        }
      });
    }
  }

  // Adds drawn points markers and labels
  drawnPoints.forEach(index => {
    const wavelength = wavelengths[index];
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

    if (showLabels) {
      chartData.push({
        x: [purpleXValues[index]],
        y: [purpleYValues[index]],
        type: 'scatter',
        mode: 'text',
        text: [`${wavelength}c`],
        textposition: 'bottom right',
        textfont: {
          color: 'black',
          size: 12
        }
      });
    }
  });

  // Adds arch data if available
  if (computedData.plsArchData) {
    const xValues = computedData.plsArchData.map(item => item[1]);
    const yValues = computedData.plsArchData.map(item => item[2]);

    // Range for the plot axes
    const minX = 0 - 0.05;
    const maxX = 1 + 0.05;
    const minY = 0 - 0.05;
    const maxY = 1 + 0.05;

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
      // Render Plot component with configured layout and checkboxes
      return (
        <div>
          <Plot
            data={chartData}
            layout={{
              width: 800,
              height: 600,
              title: plotTitle,
              xaxis: {
                title: 'Chromaticity x',
                range: [minX, maxX],
                showgrid: showGrid,
                gridcolor: 'rgba(0, 0, 0, 0.3)',
                showline: true,
                linecolor: 'black',
                linewidth: 2,
                mirror: true
              },
              yaxis: {
                title: 'Chromaticity y',
                range: [minY, maxY],
                showgrid: showGrid,
                gridcolor: 'rgba(0, 0, 0, 0.3)',
                showline: true,
                linecolor: 'black',
                linewidth: 2,
                mirror: true
              },
              autosize: false,
              margin: { l: 85, r: 85, b: 60, t: 75, pad: 4 },
              showlegend: false
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
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={showLabels}
                onChange={() => setShowLabels(!showLabels)}
              />
              Show Labels
            </label>
          </div>
        </div>
      );
    } catch (error) {
      console.error("Error rendering plot:", error);
      return <div>Error displaying plot. Please check the console for more details.</div>;
    }
  }
};

export default XyConeFundamentalBasedChromaticityDiagramPls;
