import { Data } from 'plotly.js';

export interface PlotUtilsConfig {
  startWavelength: number;
  endWavelength: number;
  step: number;
  additionalWavelengths: number[];
  purpleLineIndex: { x: number, y: number };
  whitePointIndex: { x: number, y: number };
  plotDataIndices: { x: number, y: number };
}

// Function to add specific wavelength points for highlighting
export function addSpecificWavelengthPoints(wavelengths: number[], config: PlotUtilsConfig): number[] {
  const drawnPoints: number[] = [0, wavelengths.length - 1]; // Default first and last points

  for (let wavelength = config.startWavelength; wavelength <= config.endWavelength; wavelength += config.step) {
    const index = wavelengths.indexOf(wavelength);
    if (index !== -1) {
      drawnPoints.push(index);
    }
  }

  config.additionalWavelengths.forEach(wavelength => {
    const index = wavelengths.indexOf(wavelength);
    if (index !== -1) {
      drawnPoints.push(index);
    }
  });

  return drawnPoints;
}

// Function to prepare chart data, including purple line and white point
export function prepareChartData(plotData: number[][], drawnPoints: number[], config: PlotUtilsConfig, purpleLineData?: number[][], whitePointData?: number[]): Data[] {
  const xValues = plotData.map(item => item[config.plotDataIndices.x]);
  const yValues = plotData.map(item => item[config.plotDataIndices.y]);
  const chartData: Data[] = [{
    x: xValues,
    y: yValues,
    type: 'scatter',
    mode: 'lines',
    line: { color: 'black', width: 2 }
  }];

  // Adding the purple line if available
  if (purpleLineData) {
    const purpleXValues = purpleLineData.map(item => item[config.purpleLineIndex.x]);
    const purpleYValues = purpleLineData.map(item => item[config.purpleLineIndex.y]);

    chartData.push({
      x: purpleXValues,
      y: purpleYValues,
      type: 'scatter',
      mode: 'lines',
      line: { color: 'purple', width: 2 }
    });
  }

  // Adding the white point if available
  if (whitePointData) {
    const whiteX = [whitePointData[config.whitePointIndex.x]];
    const whiteY = [whitePointData[config.whitePointIndex.y]];

    chartData.push({
      x: whiteX,
      y: whiteY,
      type: 'scatter',
      mode: 'markers',
      marker: { color: 'red', symbol: 'x-thin', size: 10, line: { color: 'black', width: 1 }}
    });
  }

  // Adding markers for specific points
  drawnPoints.forEach((index: number) => {
    chartData.push({
      x: [xValues[index]],
      y: [yValues[index]],
      type: 'scatter',
      mode: 'markers',
      marker: { color: 'white', size: 10, line: { color: 'black', width: 2 }, symbol: 'circle' }
    });
  });

  return chartData;
}

