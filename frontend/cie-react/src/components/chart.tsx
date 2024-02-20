import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

//Function for fetching data from backend endpoint and plotting the data
const FetchedChart = () => {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/compute_LMS_plots_default_data');
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
      }
    };

    fetchData();
  }, []);

  return (
    <LineChart width={600} height={300} data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="xValue" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="y1" stroke="#8884d8" />
      <Line type="monotone" dataKey="y2" stroke="#82ca9d" />
      <Line type="monotone" dataKey="y3" stroke="#ffc658" />
    </LineChart>
  );
};

export default FetchedChart;
