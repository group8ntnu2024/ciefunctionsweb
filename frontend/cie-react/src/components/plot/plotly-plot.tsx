import React from 'react';
import Plot from 'react-plotly.js';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';
import { useContentController } from '../../hooks/useContentController';
import { MethodOption, titles } from '../../utils/propTypes'

type PlotlyPlot = {
  x: number[];
  y: number[];
  type: 'scatter';
  mode: 'lines' | 'markers';
  name: string;
  marker: { color: string };
}[];

const PlotlyPlot: React.FC = () => {
  const { computedData, isLoading } = useParameters();
  const { selectedOption } = useContentController();

  const plotTitle = (selectedOption in titles) ? titles[selectedOption as MethodOption] : 'Select a method';

  const xValues = computedData.plotData.map(item => item[0]); 
  const y1Values = computedData.plotData.map(item => item[1]);
  const y2Values = computedData.plotData.map(item => item[2]);
  const y3Values = computedData.plotData.map(item => item[3]);

  const chartData: PlotlyPlot = [
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
    <Plot
      data={chartData}
      layout={{
        width: 800,
        height: 600,
        title: plotTitle,
        xaxis: { title: 'Wavelength (nm)' },
        yaxis: { title: 'Relative energy sensitivities' }
      }}
      config={{
        scrollZoom: true,
        displaylogo: false
      }}
    />
  );
};

export default PlotlyPlot;
