import React from 'react';
import ParametersForm from './ParametersFormComponent';
import { PulldownMenu } from '../PulldownMenu/PulldownMenuComponent';
import './parameters-form.css';

/**
 * Interface to define the props for ParametersLayoutComponent
 */
interface LayoutProps {
  children?: React.ReactNode;
}
/**
 * React functional component that creates a layout for displaying parameter related UI elements.
 * Wraps children, which as per implementation means that plot and sidemenu can be wrapped, allowing
 * for dynamic rendering of children components.
 * 
 * Also displays parametersform and pulldownmenu for allowing the user to specify parameters
 * and selecting which colormatch function to inspect. 
 * @param {LayoutProps} props  
 * @returns {JSX.Element} ParametersLayoutCompontent as a JSX Element. Dynamically renders children, then
 * PulldownMenu and ParametersForm
 */
const ParametersLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <>
      {children}
      <div className="parameterCard">
        <PulldownMenu />
        <ParametersForm  />
      </div>
    </>
  );
};
export default ParametersLayout;