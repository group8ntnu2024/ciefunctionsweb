import React from 'react';
import ParametersForm from './ParametersFormComponent';
import { PulldownMenu } from '../PulldownMenu/PulldownMenuComponent';
import styles from './ParametersForm.module.css';


interface LayoutProps {
  children?: React.ReactNode;
}

const ParametersLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <>
      {children}
      <div className={styles.parameterCard}>
        <PulldownMenu />
        <ParametersForm  />
      </div>
    </>
  );
};

export default ParametersLayout;