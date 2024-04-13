import { useState } from 'react';

/**
 * Hook for loading indicator. Modularized to be re-usable for multiple components. 
 *   isLoading: Boolean, stating whether component is loading or not
 *   startLoading: void,  Function to set loading state to true.
 *   stopLoading: void, Function to set loading state to false.
 */
export const useLoading = () => {
  const [isLoading, setIsLoading] = useState(true);

  const startLoading = () => setIsLoading(true);
  const stopLoading = () => setIsLoading(false);

  return {
    isLoading,
    startLoading,
    stopLoading
  };
};