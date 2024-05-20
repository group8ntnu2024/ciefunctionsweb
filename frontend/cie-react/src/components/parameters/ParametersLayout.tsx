import React from 'react';
import ParametersForm from './ParametersFormComponent';
import { PulldownMenu } from '../PulldownMenu/PulldownMenuComponent';
import './Parameters-form.css';


interface LayoutProps {
  children?: React.ReactNode;
}

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