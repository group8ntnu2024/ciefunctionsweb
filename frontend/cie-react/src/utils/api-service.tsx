import { ApiResponse, Parameters } from "./prop-types";
import { stringBuilder } from "./string-builder";



/**
 * Fetches data from the backend API.
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

async function fetchHtmlContent(endpoint: string, params: Parameters): Promise<string> {
  const url = stringBuilder(endpoint, params)
  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Accept': 'text/html' },
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  console.log(response)
  return response.text();
}
export {fetchHtmlContent}

