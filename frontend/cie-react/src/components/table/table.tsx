import '../app-content.css';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';


/**
 * A class to construct the table with the  computed data. Gets computed 
 */
const FetchedTable = () => {
  const { computedData, isLoading } = useParameters();

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
          {computedData.tableData.map((row, index) => (
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
