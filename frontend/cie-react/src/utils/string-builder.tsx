import { API_BASE_URL } from "./api-urls";
import { paramProps } from "./prop-types";

function stringBuilder(endpoint: string, params: paramProps): string {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
            queryParams.append(key, value.toString());
        }
    });
  
    return `${API_BASE_URL}${endpoint}?${queryParams.toString()}`;
  }
  export { stringBuilder};