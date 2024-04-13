import React from 'react';
import { useParameters } from '../../context/parameter-context';
import { fetchCalculationResults } from '../../utils/ApiService';
import { useLoading } from '../../hooks/useLoading';

const ParametersForm = () => {
  const { parameters, setParameters } = useParameters();
  const { startLoading, stopLoading } = useLoading();

  const handleParameterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setParameters((prev) => ({ ...prev, [name]: parseFloat(value) }));
  };

  const handleComputeClick = async () => {
    startLoading();
    try {
      const resultData = await fetchCalculationResults({
        ...parameters,
        type: "specific_computation",
      });
      window.dispatchEvent(new CustomEvent('updateTableData', { detail: resultData }));
    } catch (error) {
      console.error('Error:', error);
    } finally {
      stopLoading();
    }
  };


  return (
    <div className="parameters-form">
      <div className="parameter-control">
        <label htmlFor="field_size">Field Size:</label>
        <input
          type="number"
          id="field_size"
          name="field_size"
          value={parameters.field_size}
          onChange={handleParameterChange}
        />
      </div>
      <div className="parameter-control">
        <label htmlFor="age">Age:</label>
        <input
          type="number"
          id="age"
          name="age"
          value={parameters.age}
          onChange={handleParameterChange}
        />
      </div>
      <div className="parameter-control">
        <label htmlFor="domain_min">Domain:</label>
        <input
          type="number"
          id="domain_min"
          name="min"
          value={parameters.min}
          onChange={handleParameterChange}
        />
      </div>
      <div className="parameter-control">
        <label htmlFor="domain_max">-</label>
        <input
          type="number"
          id="domain_max"
          name="max"
          value={parameters.max}
          onChange={handleParameterChange}
        />
      </div>
      <div className="parameter-control">
        <label htmlFor="step">Step:</label>
        <input
          type="number"
          id="step"
          name="step"
          value={parameters.step}
          onChange={handleParameterChange}
        />
      </div>
      <button onClick={handleComputeClick}>Compute</button>
    </div>
  );
};

export default ParametersForm;
