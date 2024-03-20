import { useState, useEffect } from 'react';
import { fetchCalculationResults } from '../utils/ApiService';
import { paramProps } from '../utils/propTypes';

export function useFetchData(params: paramProps) {
  const [data, setData] = useState<number[][] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const result = await fetchCalculationResults(params);
        setData(result);
      } catch (error) {
        setError(error as Error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [params]);

  return { data, isLoading, error };
}