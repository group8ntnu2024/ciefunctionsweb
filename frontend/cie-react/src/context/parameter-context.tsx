import { createContext, useContext, useState, ReactNode, Dispatch, SetStateAction } from 'react';

interface Parameters {
  field_size: number;
  age: number;
  min: number;
  max: number;
  step: number;
}

interface ParametersContextType {
  parameters: Parameters;
  setParameters: Dispatch<SetStateAction<Parameters>>;
}

const defaultContextValue: ParametersContextType = {
  parameters: {
    field_size: 2.0,
    age: 32,
    min: 390.0,
    max: 830.0,
    step: 1.0,
  },
  setParameters: () => {},
};

const ParametersContext = createContext<ParametersContextType>(defaultContextValue);

export const useParameters = () => useContext(ParametersContext);

interface ParametersProviderProps {
  children: ReactNode;
}

export const ParametersProvider = ({ children }: ParametersProviderProps) => {
  const [parameters, setParameters] = useState<Parameters>(defaultContextValue.parameters);

  return (
    <ParametersContext.Provider value={{ parameters, setParameters }}>
      {children}
    </ParametersContext.Provider>
  );
};