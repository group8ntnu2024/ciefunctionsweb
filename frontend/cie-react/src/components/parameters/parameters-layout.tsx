import React from 'react';
import ParametersForm from './parameters-form';

interface LayoutProps {
  children?: React.ReactNode;
}

const ParametersLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <>
      <div>{children}</div>
      <ParametersForm  />
    </>
  );
};

export default ParametersLayout;