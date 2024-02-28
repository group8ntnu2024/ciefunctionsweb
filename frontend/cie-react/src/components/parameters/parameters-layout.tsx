import React from 'react';
import ParametersForm from './parameters-form'; // Ensure this is the correct path


interface LayoutProps {
    children: React.ReactNode;
  }
  const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
      <>
        <div>{children}</div>
        <ParametersForm />
      </>
    );
  };
  
  export default Layout;