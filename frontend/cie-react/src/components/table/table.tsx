import { useState, useEffect } from 'react';
import '../app-content.css';
import { useLoading } from '../../hooks/useLoading';
import LoadingIndicator from '../LoadingIndicator';



type data = number[][];

const FetchedTable = () => {
  const [tableData, setTableData] = useState<data>([]);
  const { isLoading, stopLoading } = useLoading();

  useEffect(() => {
    
    const handleDataUpdate = (event: CustomEvent<data>) => {
      setTableData(event.detail);
      stopLoading();
    };

    window.addEventListener('updateTableData', handleDataUpdate as EventListener);

    return () => {
      window.removeEventListener('updateTableData', handleDataUpdate as EventListener);
    };
  }, [stopLoading]);

  if (isLoading) {
    return <LoadingIndicator />;
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
