import React from 'react';
import ParametersForm from './parameters-form';

interface LayoutProps {
  selectedOption: string;
  children?: React.ReactNode;
}

const ParametersLayout: React.FC<LayoutProps> = ({ selectedOption, children }) => {
  return (
    <>
      <div>{children}</div>
      <ParametersForm selectedOption={selectedOption} />
    </>
  );
};

export default ParametersLayout;