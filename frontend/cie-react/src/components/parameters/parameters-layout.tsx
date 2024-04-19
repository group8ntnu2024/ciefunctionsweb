import React from 'react';
import ParametersForm from './parameters-form';

interface LayoutProps {
  children?: React.ReactNode;
}

const ParametersLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <>
      {children}
      <ParametersForm  />
    </>
  );
};

export default ParametersLayout;