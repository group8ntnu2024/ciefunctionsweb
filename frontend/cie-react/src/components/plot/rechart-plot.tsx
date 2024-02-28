import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend } from 'recharts';

//Function for fetching data from backend endpoint and plotting the data
const RechartPlot = () => {
  const [chartData, setChartData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);


  //TODO: implementere hooks for useeffect
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/LMS_plots');
        const json = await response.json();
        
        // Parse and transform 
        const transformedData = json.plots.map((item: any[]) => ({
          xValue: item[0],
          y1: item[1],
          y2: item[2],
          y3: item[3],
        }));
        
        setChartData(transformedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally{
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  //TODO: modularize isLoading to easily apply on every component
  if (isLoading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '600px', 
        fontSize: '20px' 
      }}>
        Loading ...
      </div>
    ); 
  }

  return (
    <LineChart width={800} height={600} data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
      <XAxis dataKey="xValue" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="y1" stroke="#FF0000"  strokeWidth={1}/>
      <Line type="monotone" dataKey="y2" stroke="#00FF00" />
      <Line type="monotone" dataKey="y3" stroke="#0000FF" />
    </LineChart>
  );
};

export default RechartPlot;
