import { ALL_SPECIFIC_DATA, BASE_URL, DEFAULT_DATA, SANIC_BASE_URL } from "./ApiUrls";
import { ApiResponse, paramProps } from "./propTypes";



/**
 * Fetches data from the backend API.
 */
async function fetchApiData(endpoint: string, params: paramProps): Promise<ApiResponse> {
  const queryParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) {
      queryParams.append(key, value.toString());
    }
  });


  const url = `${SANIC_BASE_URL}${endpoint}?${queryParams.toString()}`;
  console.log(url)
  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json().then(data => {
    if (data.result && data.plot) {
      //console.log(data.result)
      console.log(data.plot)
      return { result: data.result, plot: data.plot };
    } else {
      throw new Error('Unexpected response structure');
    }
  });
}
export {fetchApiData}

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