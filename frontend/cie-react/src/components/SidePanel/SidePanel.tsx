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
          case "method4":
            return (
              <div className="content">
                <h2>Maxwellian lm chromaticity diagram</h2>
              </div>
            );
          case "method5":
            return (
              <div className="content">
                <h2>CIE XYZ cone-fundamental-based tristimulus functions</h2>
              </div>
            );
          case "method6":
            return (
              <div className="content">
                <h2>CIE xy cone-fundamental-based chromaticity diagram</h2>
              </div>
            );
          case "method7":
            return (
              <div className="content">
                <h2>XYZ cone-fundamental-based tristimulus functions for purple-line stimuli</h2>
              </div>
            );
          case "method8":
            return (
              <div className="content">
                <h2>xy cone-fundamental-based chromaticity diagram (purple-line stimuli)</h2>
              </div>
            );
          case "method9":
            return (
              <div className="content">
                <h2>CIE XYZ standard colour-matching functions</h2>
              </div>
            );
          case "method10":
            return (
              <div className="content">
                <h2>CIE xy standard chromaticity diagram</h2>
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


