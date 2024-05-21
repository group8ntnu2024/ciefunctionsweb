import { ReactNode, createContext, useContext, useState } from 'react';

/**
 * Defines the shape of the hook returned by conent controller context
 * @property {string} selectedOption Currently selected option for color match function.
 * @property {function} setSelectedOption Function to update the selected option.
 */
type UseContentControllerHook = {
  selectedOption: string;
  setSelectedOption: (option: string) => void;
};

const ContentControllerContext = createContext<UseContentControllerHook | undefined>(undefined);

/**
 * Provider component that manages state related to the selected option for  function.
 * Wraps children to allow access for the context value.
 * @param {ReactNode} children child components that will get access to context values.
 * @returns {JSX.Element} Provider component as JSX Element that provides context values regarding selectod method for its children.
 */
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