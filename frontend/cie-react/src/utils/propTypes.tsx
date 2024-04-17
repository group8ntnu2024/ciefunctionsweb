import { Dispatch, SetStateAction } from "react";

export type paramProps = {
    field_size: number,
    age?: number,
    min?: number,
    max?: number,
    step_size?: number,
    optional?: string
}

export interface Parameters {
    field_size: number;
    age: number;
    min: number;
    max: number;
    step_size: number;
  }

export interface ComputedData {
  tableData: number[][];
  plotData: number[][];
}

export interface ParametersContextType {
    parameters: Parameters;
    setParameters: Dispatch<SetStateAction<Parameters>>;
    computedData: ComputedData;
    setComputedData: Dispatch<SetStateAction<ComputedData>>;
    computeData: () => Promise<void>;
    isLoading: boolean;
    endpoint: string;
    setEndpoint: (url: string) => void;
  }

export interface ApiResponse {
    result: number[][];
    plot: number[][];
  }

export const endpointMap: Record<string, string> = {
  method1: "lms/",
  method3: "lms-mb/",
  method7: "xy-p/"
};
  

