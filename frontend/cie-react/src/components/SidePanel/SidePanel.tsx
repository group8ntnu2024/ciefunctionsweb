import React from 'react';
import './SidePanel.css';
import 'katex/dist/katex.min.css';
import { InlineMath } from 'react-katex';
import 'katex/dist/katex.min.css';

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
                <p><strong>Parameters</strong></p>
                <p>Field size: 2°<br/>
                Age: 32 yr</p>
                <p><strong>Function symbols</strong></p>
                <p>Functions:</p>
                <InlineMath math={'\\bar{l}_{2,32} \\quad \\bar{m}_{2,32} \\quad \\bar{s}_{2,32}'} />
                <p>Argument: λ (wavelength)</p>
                <p><strong>Wavelengths</strong></p>
                <p>Domain: 390 nm – 830 nm<br/>
                Step: 1 nm</p>
                <p><strong>Normalization</strong></p>
                <p>Function values peaking at unity at 0.1 nm resolution</p>
                <p><strong>Precision of tabulated values</strong></p>
                <p>6 significant figures</p>
              </div>
            );
          case "method2":
            return (
              <div>
                <h2>CIE LMS cone fundamentals</h2>
                <p><strong>Parameters</strong></p>
                <p>Field size: 2°<br/>
                Age: 32 yr</p>
                <p><strong>Function symbols</strong></p>
                <p>Functions:</p>
                <InlineMath math={'\\bar{l}_{2,32} \\quad \\bar{m}_{2,32} \\quad \\bar{s}_{2,32}'} />
                <p>Argument: λ (wavelength)</p>
                <p><strong>Wavelengths</strong></p>
                <p>Domain: 390 nm – 830 nm<br/>
                Step: 1 nm</p>
                <p><strong>Normalization</strong></p>
                <p>Function values peaking at unity at 0.1 nm resolution</p>
                <p><strong>Precision of tabulated values</strong></p>
                <p>9 significant figures</p>
              </div>
            );
            case "method3":
              return (
                <div className="content">
                  <h2>MacLeod–Boynton ls chromaticity diagram</h2>
                  <p><strong>Parameters</strong></p>
                  <p>Field size: 2°<br/>
                  Age: 32 yr</p>
                  <p><strong>Coordinate symbols</strong></p>
                  <InlineMath math={'\\ell_{MB,2,32}, m_{MB,2,32}, s_{MB,2,32}'} />
                  <p><strong>Wavelengths</strong></p>
                  <p>Domain: 390 nm – 830 nm<br/>
                  Step: 1 nm</p>
                  <p><strong>Normalization</strong></p>
        
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
