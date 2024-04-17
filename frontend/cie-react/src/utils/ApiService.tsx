import { ALL_SPECIFIC_DATA, BASE_URL, DEFAULT_DATA, LMS_URL, SANIC_BASE_URL } from "./ApiUrls";
import { paramProps } from "./propTypes";



/**
 * Fetches LMS data from the backend API.
 */
async function fetchLMSData(params: paramProps): Promise<number[][]> {
  const queryParams = new URLSearchParams();
  queryParams.append('field_size', params.field_size.toString());
  queryParams.append('age', params.age.toString());

  if (params.min !== undefined) queryParams.append('min', params.min.toString());
  if (params.max !== undefined) queryParams.append('max', params.max.toString());
  if (params.step !== undefined) queryParams.append('step_size', params.step.toString());
  if (params.optional) queryParams.append('optional', params.optional);

  const url = `${SANIC_BASE_URL}${LMS_URL}?${queryParams.toString()}`;

  try {
    const response = await fetch(url, {
      
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    console.log(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result.result;
  } catch (error) {
    console.error('Error fetching LMS data:', error);
    throw error;
  }
}

export { fetchLMSData };

/**
 * 
 * Deprecated function. Used under development for testing plot/table in frontend
 */
async function fetchCalculationResults(params: paramProps) {
    try {
      const response = await fetch(`${BASE_URL}${ALL_SPECIFIC_DATA}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.json();
      return result.results.LMS; 
    } catch (error) {
      console.error('Error during fetch operation:', error);
      throw error;
    }
}
/**
 * Deprecated function. Used under development for testing plot/table in frontend
 * 
 */  
async function fetchDefaultData() {
  try {
      const response = await fetch(`${BASE_URL}${DEFAULT_DATA}`, {
          method: 'GET',
      });
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      return result.results.LMS;
  } catch (error) {
      console.error('Error fetching default data:', error);
      throw error;
  }
}
  
  export { fetchCalculationResults, fetchDefaultData };