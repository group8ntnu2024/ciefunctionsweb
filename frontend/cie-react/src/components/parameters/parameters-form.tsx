import React from 'react';
import { useParameters } from '../../context/parameter-context';

const ParametersForm = () => {
  const { parameters, setParameters } = useParameters();

  const handleParameterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setParameters((prev) => ({ ...prev, [name]: parseFloat(value) }));
  };

  const handleComputeClick = async () => {
    const computationParams = {
      ...parameters,
      type: "specific_computation"
    };

    try {
      const response = await fetch('http://localhost:5000/compute_all_specific_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(computationParams),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      console.log(result);
      
      const updateEvent = new CustomEvent('updateTableData', { detail: result.results.LMS });
      window.dispatchEvent(updateEvent);

    } catch (error) {
      console.error('Error during fetch operation:', error);
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
