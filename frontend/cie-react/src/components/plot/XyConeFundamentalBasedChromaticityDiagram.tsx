import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';
import { useContentController } from '../../hooks/useContentController';
import { MethodOption, titles } from '../../utils/propTypes';
import { addSpecificWavelengthPoints, prepareChartData, PlotUtilsConfig } from './plotUtils';
import './props.css';

const XyConeFundamentalBasedChromaticityDiagram: React.FC = () => {
    const { computedData, isLoading } = useParameters();
    const { selectedOption } = useContentController();
    const [showGrid, setShowGrid] = useState(true);
    const [showLabels, setShowLabels] = useState(false);
  
    if (!computedData || !computedData.plotData || computedData.plotData.length === 0) {
      return <div>No data available for plotting.</div>;
    }
  
    if (isLoading) {
      return <LoadingIndicator />;
    }
  
    const wavelengths = computedData.plotData.map(item => item[0]);
  
    // Configuration for plot utilities
    const plotConfig: PlotUtilsConfig = {
      startWavelength: 470,
      endWavelength: 611,
      step: 10,
      additionalWavelengths: [700],
      purpleLineIndex: { x: 1, y: 2 },
      whitePointIndex: { x: 0, y: 2 },
      plotDataIndices: { x: 1, y: 2 }
    };
    
  
    // Draw points according to specific wavelengths
    const drawnPoints = addSpecificWavelengthPoints(wavelengths, plotConfig);
  
    // Prepare chart data including the purple line and white point
    const chartData = prepareChartData(computedData.plotData, drawnPoints, plotConfig, computedData.purpleLineData, computedData.whitePointData);
  
    const plotTitle = selectedOption && titles[selectedOption as MethodOption] ? titles[selectedOption as MethodOption] : 'Chromaticity Diagram';
  
    let annotations = [];
    if (computedData.whitePointData && showLabels) {
      annotations.push({
        x: computedData.whitePointData[0],
        y: computedData.whitePointData[2],
        text: 'T',
        font: {
          family: 'Arial',
          size: 16,
          color: 'black'
        },
        showarrow: false,
        xshift: 10,
        yshift: 10
      });
  
      drawnPoints.forEach(index => {
        const wavelength = wavelengths[index];
        const x = computedData.plotData[index][plotConfig.plotDataIndices.x];
        const y = computedData.plotData[index][plotConfig.plotDataIndices.y];
        annotations.push({
          x: x,
          y: y,
          text: `${wavelength}`,
          font: {
            family: 'Arial',
            size: 12,
            color: 'black'
          },
          showarrow: false,
          xshift: 10,
          yshift: 10
        });
      });
    }
  
    // Range range for the plot axes
    const minX = 0 - 0.05;
    const maxX = 1 + 0.05;
    const minY = 0 - 0.05;
    const maxY = 1 + 0.05;
  
    try {
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
              annotations: annotations,
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
  };


export default XyConeFundamentalBasedChromaticityDiagram;
