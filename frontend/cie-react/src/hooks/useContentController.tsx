import { useState } from 'react';

type UseContentControllerHook = {
  selectedOption: string;
  setSelectedOption: (option: string) => void;
};

function useContentController(initialOption: string = "method1"): UseContentControllerHook {
  const [selectedOption, setSelectedOption] = useState<string>(initialOption);

  return {
    selectedOption,
    setSelectedOption,
  };
}

export default useContentController;