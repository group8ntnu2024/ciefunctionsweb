import './table.css';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';


/**
 * React functinoal component to construct the table with the computed data.
 * Takes the JSON response from the api call and puts the result.data into 
 * the table
 * @returns {JSX.Element} TableContent as JSX Element
 */
const TableContent = () => {
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


export default TableContent;
