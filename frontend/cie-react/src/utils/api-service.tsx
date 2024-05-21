import { ApiResponse, Parameters } from "./prop-types";
import { stringBuilder } from "./string-builder";



/**
 * Fetches data from the backend API.
 * 
 * Constructs url with the help of the stringbuilder utils function and the parameters
 * 'endpoint' and 'params' that it receives. Makes a GET request to the bakcend API
 * at the constructed URL
 * @param {string} endpoint The API endpoint to fetch data from. This corresponds to the selected color match function
 * @param {Parameters} params The user specified parameters to be included in the API request
 * @returns {Promise<ApiResponse>} Returns the result from the API request and promises the format to correspond to ApiRespone
 */
async function fetchApiData(endpoint: string, params: Parameters): Promise<ApiResponse> {
  const url = stringBuilder(endpoint, params);
  console.log(url);
  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json().then(data => {
    if (data.result && data.plot) {
      return { result: data.result};
    } else {
      throw new Error('Unexpected response structure');
    }
  });
}
export {fetchApiData}

