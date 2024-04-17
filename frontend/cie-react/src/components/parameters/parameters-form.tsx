import React, { ChangeEvent, useEffect } from 'react';
import { useParameters } from '../../context/parameter-context';

interface ParametersFormProps {
  selectedOption: string;
}

const ParametersForm: React.FC<ParametersFormProps> = ({ selectedOption }) => {
  const { parameters, setParameters, computeData } = useParameters();

  useEffect(() => {
    console.log("Selected method:", selectedOption);
  }, [selectedOption]);

  const handleParameterChange = (event: ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = event.target;
    setParameters(prev => ({ ...prev, [name]: parseFloat(value) }));
  };

  const createParameterControl = (label: string, name: string, value: number, onChange: (event: ChangeEvent<HTMLInputElement>) => void) => (
    <div className="parameters-control d-flex align-items-center">
      <label htmlFor={name} className="mb-0">{label}</label>
      <input
        type="number"
        className="form-control"
        id={name}
        name={name}
        value={value.toString()}
        onChange={onChange}
      />
    </div>
  );

  const renderParameters = () => {
    switch (selectedOption) {
      case "method1":
      case "method2":
        return (
          <div className="d-flex align-items-center flex-grow-1">
            {createParameterControl("Field Size:", "field_size", parameters.field_size, handleParameterChange)}
            {createParameterControl("Age:", "age", parameters.age, handleParameterChange)}
            {createParameterControl("Domain Min:", "min", parameters.min, handleParameterChange)}
            {createParameterControl("Domain Max:", "max", parameters.max, handleParameterChange)}
            {createParameterControl("Step:", "step", parameters.step, handleParameterChange)}
          </div>
        );
      default:
        return <p>Please select a method to display parameters.</p>;
    }
  };

  return (
    <div className="d-flex justify-content-between align-items-center w-100 parameters-form">
      <div className="flex-grow-1 d-flex justify-content-start">
        {renderParameters()}
      </div>
      <button className="btn btn-primary ml-2" onClick={computeData}>Compute</button>
    </div>
  );
};

export default ParametersForm;
