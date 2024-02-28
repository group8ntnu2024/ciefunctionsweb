import{ useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

type MyPlotData = {
    x: any[];
    y: any[];
    type: 'scatter';
    mode: 'lines';
    name: string;
    marker: { color: string };
  }[];
  
  const PlotlyPlot = () => {
    const [chartData, setChartData] = useState<MyPlotData>([]);
    const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/LMS_plots');
        const json = await response.json();
        
        const xValues = json.plots.map((item: any[]) => item[0]);
        const y1Values = json.plots.map((item: any[]) => item[1]);
        const y2Values = json.plots.map((item: any[]) => item[2]);
        const y3Values = json.plots.map((item: any[]) => item[3]);

        setChartData([
          { x: xValues, y: y1Values, type: 'scatter', mode: 'lines', name: 'Y1', marker: {color: 'red'} },
          { x: xValues, y: y2Values, type: 'scatter', mode: 'lines', name: 'Y2', marker: {color: 'green'} },
          { x: xValues, y: y3Values, type: 'scatter', mode: 'lines', name: 'Y3', marker: {color: 'blue'} }
        ]);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return <div>Loading ...</div>;
  }

  return (
    <Plot
      data={chartData}
      layout={{
        width: 800, 
        height: 600, 
        title: 'LMS',
        xaxis: { title: 'Wavelength (nm)' },
        yaxis: { title: 'Relative energy sensitivities' }
      }}
    />
  );
};

export default PlotlyPlot;
