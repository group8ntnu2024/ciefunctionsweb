import React from 'react';
import './SidePanel.css';

interface SidePanelProps {
  selectedOption: string;
}

export const SidePanel: React.FC<SidePanelProps> = ({ selectedOption }) => {
    const renderFormula = () => {
        switch (selectedOption) {
          case "method1":
            return (
              <div>
                <h2>CIE LMS cone fundamentals</h2>
                <p>6 significant figures</p>
              </div>
            );
          case "method2":
            return (
              <div>
                <h2>CIE LMS cone fundamentals</h2>
                <p>9 significant figures</p>
              </div>
            );
            case "method3":
              return (
                <div className="content">
                  <h2>MacLeod–Boynton ls chromaticity diagram</h2>
                </div>
              );
          default:
            return <p>Select a method to see its formula.</p>;
        }
      };
      
      return (
        <div className="sidePanel">
          {renderFormula()}
        </div>
      );
};


