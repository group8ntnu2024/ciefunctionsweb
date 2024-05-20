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
  tableData: number[][];}

export interface ParametersContextType {
    parameters: Parameters;
    setParameters: Dispatch<SetStateAction<Parameters>>;
    computedData: ComputedData;
    setComputedData: Dispatch<SetStateAction<ComputedData>>;
    computeData: () => Promise<void>;
    isLoading: boolean;
    endpoint: string;
    setEndpoint: (url: string) => void;
    plotUrl: string;
    setPlotUrl: (url:string) => void;
    sidemenuUrl: string;
    setSidemenuUrl: (url:string) => void; 
}

export interface ApiResponse {
    result: number[][];
}

export const endpointMap: Record<string, string> = {
  method1: "lms/",
  method2: "lms/",
  method3: "lms-mb/",
  method4: "lms-mw/",
  method5: "xyz/",
  method6: "xy/",
  method7: "xyz-p/",
  method8: "xy-p/",
  method9: "xyz-std/",
  method10: "xy-std/",


};

export type MethodOption = 'method1' | 'method2' | 'method3' | 'method4' | 'method5' |'method6' | 'method7' | 'method8' | 'method9' | 'method10';


export const titles: Record<MethodOption, string> = {
  method1: "CIE LMS cone fundamentals",
  method2: "CIE LMS cone fundamentals (9 sign. figs.)",
  method3: "MacLeod-Boynton Is chromaticity diagram",
  method4: "Maxwellian Im chromaticity diagram",
  method5: "CIE XYZ cone-fundamental-based tristimulus functions",
  method6: "CIE xy cone-fundamental-based chromaticity diagram",
  method7: "XYZ cone-fundamental-based tristimulus functions for purple-line stimuli",
  method8: "xy cone-fundamental-based chromaticity diagram (purple-line stimuli)",
  method9: "CIE XYZ standard colour-matching functions",
  method10: "CIE xy standard chromaticity diagram",
};
  

