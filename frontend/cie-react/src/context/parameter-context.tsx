import { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import { Parameters, ComputedData, ParametersContextType } from '../utils/propTypes';
import { fetchApiData, stringBuilder } from '../utils/ApiService';
import { useLoading } from '../hooks/useLoading';


const defaultContextValue: ParametersContextType = {
  parameters: {
    field_size: 2.0,
    age: 32,
    min: 390.0,
    max: 830.0,
    step_size: 1.0,
  },
  setParameters: () => {},
  computedData : {
    tableData: []
  },
  setComputedData: () => {},
  computeData: async () => {},
  isLoading: true,
  endpoint: '',
  setEndpoint: () => {},
  htmlContent: '',
  plotUrl: '',
  setPlotUrl: () => {},
  sidemenuUrl: '',
  setSidemenuUrl: () => {}

};

const ParametersContext = createContext<ParametersContextType>(defaultContextValue);

export const useParameters = () => useContext(ParametersContext);

export const ParametersProvider = ({ children }: { children?: ReactNode }) => {
  const [parameters, setParameters] = useState<Parameters>(defaultContextValue.parameters);
  const [computedData, setComputedData] = useState<ComputedData>(defaultContextValue.computedData);
  const [htmlContent] = useState<string>('');
  const { isLoading, stopLoading } = useLoading();
  const [endpoint, setEndpoint] = useState<string>('lms/');
  const [plotUrl, setPlotUrl] = useState<string>('');
  const [sidemenuUrl, setSidemenuUrl] = useState<string>('');

  
  const updateIframes = useCallback(async () => {
    try {
      const plotUrl = stringBuilder(endpoint + 'plot/', parameters);
      const menuUrl = stringBuilder(endpoint + 'sidemenu/', parameters);
      setPlotUrl(plotUrl);
      setSidemenuUrl(menuUrl);
    } catch (error) {
      console.error('Error fetching plot content:', error);
    }
  }, [endpoint, parameters]);

  const computeData = useCallback(async () => {
    const calculateData = endpoint + 'calculation/';
    try {
      console.log("Current parameters:", parameters);
      const { result } = await fetchApiData(calculateData, parameters);
      setComputedData({ tableData: result});
      updateIframes();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      stopLoading();
    }
  }, [endpoint, parameters]);

  return (
    <ParametersContext.Provider value={{ parameters, setParameters, computedData, setComputedData, computeData, htmlContent,isLoading, endpoint, setEndpoint, plotUrl, setPlotUrl, sidemenuUrl, setSidemenuUrl }}>
      {children}
    </ParametersContext.Provider>
  );
};
