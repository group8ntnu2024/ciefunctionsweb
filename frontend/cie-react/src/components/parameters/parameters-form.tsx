import React, { ChangeEvent, useEffect } from 'react';
import { useParameters } from '../../context/parameter-context';
import styles from './ParametersForm.module.css';
import { endpointMap } from '../../utils/propTypes';
import { LMS_CALC_URL } from '../../utils/ApiUrls';

interface ParametersFormProps {
  selectedOption: string;
}

const ParametersForm: React.FC<ParametersFormProps> = ({ selectedOption }) => {
  const { parameters, setParameters, computeData, setEndpoint } = useParameters();

  useEffect(() => {
    console.log("Selected method:", selectedOption);
    const newEndpoint = endpointMap[selectedOption] || LMS_CALC_URL;
    setEndpoint(newEndpoint);
  }, [selectedOption, setEndpoint]);

  const handleParameterChange = (event: ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = event.target;
    setParameters(prev => ({ ...prev, [name]: parseFloat(value) }));
  };

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
      >
        <option value="2">2°</option>
        <option value="10">10°</option>
      </select>
    </div>
  );

  const createParameterForm = () => {
    return(<div className={styles.parametersForm}>
      {createParameterControl("Field size:", "field_size", parameters.field_size, handleParameterChange)}
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
    let caseNumber;
    if (methodNumber >= 1 && methodNumber <= 8) {
      caseNumber = 1;
    } else if (methodNumber >= 9 && methodNumber <= 10) {
      caseNumber = 2;
    } else {
      caseNumber = 0;
    }

    switch (caseNumber) {
      case 1:
        return (
          <div>
          {createParameterForm()}
        </div>
        );
      
      case 2:
        return (
          <div className={styles.parametersForm}>
            {createDegreeDropdown()}
          </div>
        );
      default:
        return <p>Please select a method to display parameters.</p>;
    }
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
