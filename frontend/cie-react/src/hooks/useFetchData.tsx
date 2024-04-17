/*import { useState, useEffect } from 'react';
import { fetchApiData } from '../utils/ApiService';
import { paramProps } from '../utils/propTypes';

export function useFetchData(endpoint: string, params: paramProps) {
  const [data, setData] = useState<number[][] | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const result = await fetchApiData(endpoint, params);
        setData(result);
      } catch (error) {
        setError(error as Error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [endpoint, params]);

  return { data, isLoading, error };
}*/

//deprecated, keeping for potential use in future