import { SANIC_BASE_URL } from "./ApiUrls";
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
  console.log(url);
  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json().then(data => {
    const apiResponse: ApiResponse = {
      result: data.result ?? [],
      plot: data.plot ?? [],
      xyz_plot: data.xyz_plot ?? [],
      plot_purple: data.plot_purple ?? [],
      plot_white: data.plot_white ?? [],

    };
    return apiResponse;
  });
}
export {fetchApiData}

async function fetchHtmlContent(endpoint: string, params: paramProps): Promise<string> {
  const queryParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) {
      queryParams.append(key, value.toString());
    }
  });

  const url = `${SANIC_BASE_URL}${endpoint}?${queryParams.toString()}`;
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

function stringBuilder(endpoint: string, params: paramProps): string {
  const queryParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
          queryParams.append(key, value.toString());
      }
  });

  return `${SANIC_BASE_URL}${endpoint}?${queryParams.toString()}`;
}
export { stringBuilder};