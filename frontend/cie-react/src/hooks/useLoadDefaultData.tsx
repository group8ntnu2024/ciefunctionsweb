import { useEffect, useState } from "react";
import { fetchDefaultData } from "../utils/ApiService";

function useLoadDefaultData() {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
  
    useEffect(() => {
      async function loadDefault() {
        try {
          const defaultData = await fetchDefaultData();
          setData(defaultData);
          setIsLoading(false);
        } catch (error) {
          setError(error as Error);
          setIsLoading(false);
        }
      }
  
      loadDefault();
    }, []);
  
    return { data, isLoading, error };
  }
  
  export default useLoadDefaultData;