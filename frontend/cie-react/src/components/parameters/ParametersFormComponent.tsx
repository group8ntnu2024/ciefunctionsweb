import React, { ChangeEvent, useEffect, useState } from 'react';
import { useParameters } from '../../context/parameter-context';
import './Parameters-form.css'
import { endpointMap } from '../../utils/prop-types';
import { LMS_URL } from '../../utils/api-urls';
import { useContentController } from '../../hooks/useContentController';
import { parameterSchema } from '../../utils/parameters-form-component-util';


const ParametersForm: React.FC = () => {
  const { parameters, setParameters, computeData, setEndpoint, endpoint } = useParameters();
  const { selectedOption } = useContentController();
  const [generalFieldSize, setGeneralFieldSize] = useState(parameters.field_size);
  const [dropdownFieldSize, setDropdownFieldSize] = useState(parameters.field_size);
  const [paramsUpdated, setParamsUpdated] = useState(false);

  //useeffect to set new endpoint based on selected option in pulldown
  useEffect(() => {
    const newEndpoint = endpointMap[selectedOption] || LMS_URL;
    setEndpoint(newEndpoint);
  }, [selectedOption, setEndpoint]);

   //useeffect to use generalFieldSize for function 1-8 and dropDownFieldSize for function 9 and 10. State handling for the two different field sizes
   useEffect(() => {
    const methodNumber = parseInt(selectedOption.replace('method', ''));
    setParameters(prev => {
      let updatedParams = { ...prev };

      // Handle optional parameter for method2
      if (selectedOption === 'method2') {
        updatedParams.optional = 'base';
      } else {
        delete updatedParams.optional;
      }

      // Handle field size based on method number
      if (methodNumber >= 1 && methodNumber <= 8) {
        updatedParams.field_size = generalFieldSize;
      } else if (methodNumber >= 9 && methodNumber <= 10) {
        updatedParams.field_size = dropdownFieldSize;
      }

      return updatedParams;
    });
    setParamsUpdated(true);
  }, [selectedOption, dropdownFieldSize, setParameters]);

  //useffect to call computedata when endpoint is changed or when dropDownFieldSize is changed
  useEffect(() => {
    if (paramsUpdated) {
      computeData();
      setParamsUpdated(false);
    }
}, [endpoint, selectedOption, paramsUpdated, setParameters]);

  //Handles parameter change for every function except xyz
  const handleParameterChange = (event: ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = event.target;
    const numericValue = parseFloat(value);
  
    parameterSchema.validateAt(name, { [name]: numericValue })
      .then(() => {
        if (name === 'field_size') {
          setGeneralFieldSize(numericValue);
        }
        setParameters(prev => ({ ...prev, [name]: numericValue }));
      })
      .catch(err => {
        console.error(err.errors);
      });
  };
  
  //Handles parameter change for xyz functions, where field size of either 2 or 10 degrees are the parameters
  const handleDropdownChange = (event: ChangeEvent<HTMLSelectElement>): void => {
    const selectedDegree = parseFloat(event.target.value);
    setDropdownFieldSize(selectedDegree);
    setParameters(prev => ({ ...prev, field_size: selectedDegree }));
    setParamsUpdated(true);
  };

  const createParameterControl = (label: string, name: string, value: number, onChange: (event: ChangeEvent<HTMLInputElement>) => void) => (
    <div className="parametersControl">
      <label className="parameterLabel" htmlFor={name}>{label}</label>
      <input
        type="number"
        className="formControl"
        id={name}
        name={name}
        value={name === "age" ? value.toString() : value.toFixed(1)}
        onChange={onChange}
        step={name === "age" ? 1 :  0.1}
      />
    </div>
  );

  const createDegreeDropdown = () => (
    <div className="parametersControl">
      <label htmlFor="degree-selection">Field size:	</label>
      <select
        className="formControl"
        id="degree-selection"
        name="degree-selection"
        value={dropdownFieldSize.toString()}
        onChange={handleDropdownChange}
      >
        <option value="2">2°</option>
        <option value="10">10°</option>
      </select>
    </div>
  );

  const createParameterForm = () => {
    return(<div className="parametersForm">
      {createParameterControl("Field size:", "field_size", generalFieldSize, handleParameterChange)}
      {createParameterControl("Age:", "age", parameters.age, handleParameterChange)}
      {createParameterControl("Domain min(nm):", "min", parameters.min, handleParameterChange)}
      {createParameterControl("Domain max (nm):", "max", parameters.max, handleParameterChange)}
      {createParameterControl("Step(nm):", "step_size", parameters.step_size, handleParameterChange)}
      <button className="btnPrimary" onClick={computeData}>Compute</button>
    </div>
    );
  }

  const renderParameters = () => {

     const methodNumber = parseInt(selectedOption.replace('method', ''));
    if (methodNumber >= 1 && methodNumber <= 8) {
      return createParameterForm();
    } else if (methodNumber >= 9 && methodNumber <= 10) {
      return createDegreeDropdown();
    }
    return <p>Please select a method to display parameters.</p>;
  };

  return (
    <div className="parametersForm">
        {renderParameters()}
    </div>
  );
};

export default ParametersForm;
