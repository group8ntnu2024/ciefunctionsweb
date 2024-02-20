import { useState, useEffect } from 'react';

const FetchedTable = () => {
  const [tableData, setTableData] = useState<number[][]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/compute_LMS_results_default_data');
        const json = await response.json();
        
        setTableData(json.results);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="scrollable-table">
      <table>
        <thead>
          <tr>
            <th>X</th>
            <th>Y 1</th>
            <th>Y 2</th>
            <th>Y 3</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map((row, index) => (
            <tr key={index}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FetchedTable;
