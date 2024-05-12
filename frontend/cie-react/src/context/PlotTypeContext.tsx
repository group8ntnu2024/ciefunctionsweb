import React, { useContext, useState, createContext, ReactNode } from 'react';

interface PlotTypeContextType {
  plotType: string;
  setPlotType: (plotType: string) => void;
}

const PlotTypeContext = createContext<PlotTypeContextType | undefined>(undefined);

export const usePlotType = (): PlotTypeContextType => {
  const context = useContext(PlotTypeContext);
  if (!context) {
    throw new Error('usePlotType must be used within a PlotTypeProvider');
  }
  return context;
};

interface PlotTypeProviderProps {
  children: ReactNode;
}

export const PlotTypeProvider: React.FC<PlotTypeProviderProps> = ({ children }) => {
  const [plotType, setPlotType] = useState<string>('defaultPlot'); // default plot type
  return (
    <PlotTypeContext.Provider value={{ plotType, setPlotType }}>
      {children}
    </PlotTypeContext.Provider>
  );
};
