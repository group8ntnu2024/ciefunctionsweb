import { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import { Parameters, ComputedData, ParametersContextType } from '../utils/prop-types';
import { fetchApiData } from '../utils/api-service';
import { useLoading } from '../hooks/useLoading';
import { stringBuilder } from '../utils/string-builder';

/**
 * Default values for the context of parameters and functions
 * related to the context of parameters.
 */
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
  plotUrl: '',
  setPlotUrl: () => {},
  sidemenuUrl: '',
  setSidemenuUrl: () => {}

};

/**
 * Creates a context with default values. Contains a set of functions to help manipulate
 * parameter state.
 * 
 * Exports ParameterProvider which wraps children and allows for state handling of
 * parameters through the applicaiton.
 */
const ParametersContext = createContext<ParametersContextType>(defaultContextValue);
export const useParameters = () => useContext(ParametersContext);
export const ParametersProvider = ({ children }: { children?: ReactNode }) => {
  const [parameters, setParameters] = useState<Parameters>(defaultContextValue.parameters);
  const [computedData, setComputedData] = useState<ComputedData>(defaultContextValue.computedData);
  const { isLoading, stopLoading } = useLoading();
  const [endpoint, setEndpoint] = useState<string>('lms/');
  const [plotUrl, setPlotUrl] = useState<string>('');
  const [sidemenuUrl, setSidemenuUrl] = useState<string>('');

  //fetches the iframe for sidemenu and plot from the backend API
  const updateIframes = useCallback(async () => {
    try {
      const plotUrl = stringBuilder(endpoint + 'plot', parameters);
      const menuUrl = stringBuilder(endpoint + 'sidemenu', parameters);
      setPlotUrl(plotUrl);
      setSidemenuUrl(menuUrl);
    } catch (error) {
      console.error('Error fetching plot content:', error);
    }
  }, [endpoint, parameters]);

  //fetches the result data from the backend API
  //to be displayed in the TableComponent
  const computeData = useCallback(async () => {
    const calculateData = endpoint + 'calculation';
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
    <ParametersContext.Provider value={{ parameters, setParameters, computedData, setComputedData, computeData, isLoading, endpoint, setEndpoint, plotUrl, setPlotUrl, sidemenuUrl, setSidemenuUrl }}>
      {children}
    </ParametersContext.Provider>
  );
};
