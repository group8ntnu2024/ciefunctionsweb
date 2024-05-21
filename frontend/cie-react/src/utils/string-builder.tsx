import { API_BASE_URL } from "./api-urls";
import { Parameters } from "./prop-types";

/**
 * Function for building the url strings based ont he variable endpoint and parameters.
 * Constructs the complete URL by appending the endpoint to the base url and adding query parameters.
 * @param endpoint The endpoint defined by the specified function.
 * @param params The parameters specified by the user.
 * @returns {string} The constructed URL as a string.
 */
function stringBuilder(endpoint: string, params: Parameters): string {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
            queryParams.append(key, value.toString());
        }
    });
  
    return `${API_BASE_URL}${endpoint}?${queryParams.toString()}`;
  }
  export { stringBuilder};