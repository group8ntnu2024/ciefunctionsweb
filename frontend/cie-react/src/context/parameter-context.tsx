import { createContext, useContext, useState, ReactNode } from 'react';
import { Parameters, ComputedData, ParametersContextType } from '../utils/propTypes';
import { fetchApiData } from '../utils/ApiService';
import { useLoading } from '../hooks/useLoading';
import { LMS_URL } from '../utils/ApiUrls';



const defaultContextValue: ParametersContextType = {
  parameters: {
    field_size: 2.0,
    age: 32,
    min: 390.0,
    max: 830.0,
    step_size: 1.0,
  },
  setParameters: () => {},
  computedData : { tableData: [] },
  setComputedData: () => {},
  computeData: async () => {},
  isLoading: true,
  endpoint: LMS_URL,
  setEndpoint: () => {}
};

const ParametersContext = createContext<ParametersContextType>(defaultContextValue);

export const useParameters = () => useContext(ParametersContext);

export const ParametersProvider = ({ children }: { children: ReactNode }) => {
  const [parameters, setParameters] = useState<Parameters>(defaultContextValue.parameters);
  const [computedData, setComputedData] = useState<ComputedData>(defaultContextValue.computedData);
  const { isLoading, startLoading, stopLoading } = useLoading();
  const [endpoint, setEndpoint] = useState<string>(LMS_URL);

  const computeData = async () => {
    try {
      startLoading();
      const resultData = await fetchApiData(endpoint, { ...parameters});
      setComputedData({ tableData: resultData });
    } catch (error) {
      console.error('Error:', error);
    } finally {
      stopLoading();
    }
  };

  return (
    <ParametersContext.Provider value={{ parameters, setParameters, computedData, setComputedData, computeData, isLoading, endpoint, setEndpoint }}>
      {children}
    </ParametersContext.Provider>
  );
};
