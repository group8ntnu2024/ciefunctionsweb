import { Dispatch, SetStateAction } from "react";

export type paramProps = {
    type: string,
    field_size: number,
    age: number,
    min: number,
    max: number,
    step: number
}

export interface Parameters {
    field_size: number;
    age: number;
    min: number;
    max: number;
    step: number;
  }

export interface ComputedData {
  tableData: number[][];
}

export interface ParametersContextType {
    parameters: Parameters;
    setParameters: Dispatch<SetStateAction<Parameters>>;
    computedData: ComputedData;
    setComputedData: Dispatch<SetStateAction<ComputedData>>;
    computeData: () => void;
    isLoading: boolean;
  }

