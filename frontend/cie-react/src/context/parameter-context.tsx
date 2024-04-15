import { createContext, useContext, useState, ReactNode } from 'react';
import { Parameters, ComputedData, ParametersContextType } from '../utils/propTypes';
import { fetchCalculationResults } from '../utils/ApiService';
import { useLoading } from '../hooks/useLoading';



const defaultContextValue: ParametersContextType = {
  parameters: {
    field_size: 2.0,
    age: 32,
    min: 390.0,
    max: 830.0,
    step: 1.0,
  },
  setParameters: () => {},
  computedData : { tableData: [] },
  setComputedData: () => {},
  computeData: () => {},
  isLoading: true
};

const ParametersContext = createContext<ParametersContextType>(defaultContextValue);

export const useParameters = () => useContext(ParametersContext);

interface ParametersProviderProps {
  children: ReactNode;
}

export const ParametersProvider = ({ children }: ParametersProviderProps) => {
  const [parameters, setParameters] = useState<Parameters>(defaultContextValue.parameters);
  const [computedData, setComputedData] = useState<ComputedData>(defaultContextValue.computedData);
  const { isLoading, startLoading, stopLoading } = useLoading();

  const computeData = async() => {
   
     try {
      startLoading();
      const resultData = await fetchCalculationResults({
        ...parameters,
        type: "specific_computation",
      });
      setComputedData({ tableData: resultData });
    } catch (error) {
      console.error('Error:', error);
    }finally{
      stopLoading();
    }
  };

  return (
    <ParametersContext.Provider value={{ parameters, setParameters, computedData, setComputedData, computeData, isLoading}}>
      {children}
    </ParametersContext.Provider>
  );
};
