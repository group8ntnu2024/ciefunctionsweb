import { useState, useEffect } from 'react';

const FetchedTable = () => {
  const [tableData, setTableData] = useState<number[][]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/LMS_results');
        const json = await response.json();
        
        setTableData(json.results);
      } catch (error) {
        console.error('Error fetching data:', error);
      }finally{
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

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
