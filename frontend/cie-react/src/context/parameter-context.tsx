import { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import { Parameters, ComputedData, ParametersContextType } from '../utils/propTypes';
import { fetchApiData, fetchHtmlContent } from '../utils/ApiService';
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
    tableData: [],
    plotData: [],
    purpleLineData: [],
    whitePointData: []
  },
  setComputedData: () => {},
  computeData: async () => {},
  isLoading: true,
  endpoint: '',
  setEndpoint: () => {},
  htmlContent: ''
};

const ParametersContext = createContext<ParametersContextType>(defaultContextValue);

export const useParameters = () => useContext(ParametersContext);

export const ParametersProvider = ({ children }: { children?: ReactNode }) => {
  const [parameters, setParameters] = useState<Parameters>(defaultContextValue.parameters);
  const [computedData, setComputedData] = useState<ComputedData>(defaultContextValue.computedData);
  const [htmlContent, setHtmlContent] = useState<string>('');
  const { isLoading, startLoading, stopLoading } = useLoading();
  const [endpoint, setEndpoint] = useState<string>('');


  const updateSideMenu = useCallback(async () => {
    try {
      const sideMenuContent = await fetchHtmlContent(endpoint + 'sidemenu/', parameters);
      setHtmlContent(sideMenuContent);
    } catch (error) {
      console.error('Error fetching sidemenu content:', error);
    }
  }, [endpoint, parameters]);

  const computeData = useCallback(async () => {
    const calculateData = endpoint + 'calculation/';
  
    startLoading();
    try {
      console.log("Current parameters:", parameters);
      const { result, plot, plot_purple, plot_white, xyz_plot } = await fetchApiData(calculateData, parameters);
      setComputedData({ 
        tableData: result, 
        plotData: plot, 
        purpleLineData: plot_purple,
        whitePointData: plot_white,
        plsArchData: xyz_plot,
      });
      await updateSideMenu();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      stopLoading();
    }
  }, [endpoint, parameters, setComputedData, updateSideMenu, startLoading, stopLoading]);

  return (
    <ParametersContext.Provider value={{ parameters, setParameters, computedData, setComputedData, computeData, htmlContent,isLoading, endpoint, setEndpoint }}>
      {children}
    </ParametersContext.Provider>
  );
};
