import { ReactNode, createContext, useContext, useState } from 'react';

type UseContentControllerHook = {
  selectedOption: string;
  setSelectedOption: (option: string) => void;
};

const ContentControllerContext = createContext<UseContentControllerHook | undefined>(undefined);

export const UseContentControllerProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedOption, setSelectedOption] = useState<string>("method1");

  return (
    <ContentControllerContext.Provider value={{ selectedOption, setSelectedOption }}>
      {children}
    </ContentControllerContext.Provider>
  );
};

export const useContentController = (): UseContentControllerHook => {
  const context = useContext(ContentControllerContext);
  if (context === undefined) {
    throw new Error('Error!! useContentController without context!!');
  }
  return context;
};