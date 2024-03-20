import { ALL_SPECIFIC_DATA, BASE_URL } from "./ApiUrls";

type paramProps = {
    type: string,
    field_size: number,
    age: number,
    min: number,
    max: number,
    step: number
}


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
  
  export { fetchCalculationResults };