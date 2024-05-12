import React, { ChangeEvent, useEffect, useState } from 'react';
import { useParameters } from '../../context/parameter-context';
import styles from './ParametersForm.module.css';
import { endpointMap } from '../../utils/propTypes';
import { LMS_CALC_URL } from '../../utils/ApiUrls';
import { useContentController } from '../../hooks/useContentController';


const ParametersForm: React.FC = () => {
  const { parameters, setParameters, computeData, setEndpoint, endpoint } = useParameters();
  const { selectedOption } = useContentController();

  //useeffect to set new endpoint based on selected option in pulldown
  useEffect(() => {
    console.log("\n -------------------------------------------------------- \n" + "Selected method:", selectedOption);
    const newEndpoint = endpointMap[selectedOption] || LMS_CALC_URL;
    setEndpoint(newEndpoint);
    console.log("endpoint: " + newEndpoint)
  }, [selectedOption, setEndpoint]);

  //useffect to call computedata when endpoint is changed
  useEffect(() => {
    if (endpoint) {
      computeData();
    }
  }, [endpoint]);

  //Different states for field size based on selected function
  const [generalFieldSize, setGeneralFieldSize] = useState(parameters.field_size);
  const [dropdownFieldSize, setDropdownFieldSize] = useState(parameters.field_size);

  //Handles parameter change for every function except xyz
  const handleParameterChange = (event: ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = event.target;
    if (name === 'field_size') {
      setGeneralFieldSize(parseFloat(value));
    }
    setParameters(prev => ({ ...prev, [name]: parseFloat(value) }));
  };

  
  //Handles parameter change for xyz functions, where field size of either 2 or 10 degrees are the parameters
  const handleDropdownChange = (event: ChangeEvent<HTMLSelectElement>): void => {
    const selectedDegree = parseFloat(event.target.value);
    setDropdownFieldSize(selectedDegree);
    setParameters(prev => ({ ...prev, field_size: selectedDegree }));
  };

  //useeffect to do api call when the field size for xyz is changed.
  useEffect(() => {
    if (dropdownFieldSize) {
      computeData();
    }
  }, [dropdownFieldSize]);

  //useeffect to use generalFieldSize for function 1-8 and dropDownFieldSize for function 9 and 10. State handling for the two different field sizes
  useEffect(() => {
    const methodNumber = parseInt(selectedOption.replace('method', ''));
    if (methodNumber >= 1 && methodNumber <= 8) {
      setParameters(prev => ({ ...prev, field_size: generalFieldSize }));
    } else if (methodNumber >= 9 && methodNumber <= 10) {
      setParameters(prev => ({ ...prev, field_size: dropdownFieldSize }));
    }
  }, [selectedOption, generalFieldSize, dropdownFieldSize]);

  const createParameterControl = (label: string, name: string, value: number, onChange: (event: ChangeEvent<HTMLInputElement>) => void) => (
    <div className={styles.parametersControl}>
      <label htmlFor={name} className={`mb-0 ${label === "-" ? styles.labelSpacing : "  "}`}>{label}</label>
      <input
        type="number"
        className={styles.formControl}
        id={name}
        name={name}
        value={value.toString()}
        onChange={onChange}
      />
    </div>
  );

  const createDegreeDropdown = () => (
    <div className={styles.parametersControl}>
      <label htmlFor="degree-selection">Field size:	</label>
      <select
        className={styles.formControl}
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
    return(<div className={styles.parametersForm}>
      {createParameterControl("Field size:", "field_size", generalFieldSize, handleParameterChange)}
      {createParameterControl("Age:", "age", parameters.age, handleParameterChange)}
      {createParameterControl("Domain(nm):", "min", parameters.min, handleParameterChange)}
      {createParameterControl("-", "max", parameters.max, handleParameterChange)}
      {createParameterControl("Step(nm):", "step_size", parameters.step_size, handleParameterChange)}
      <button className={`${styles.btnPrimary} btn`} onClick={computeData}>Compute</button>
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
    <div className={styles.parametersForm}>
      <div style={{ flex: '1 1 auto' }}>
        {renderParameters()}
      </div>
    </div>
  );
};

export default ParametersForm;
