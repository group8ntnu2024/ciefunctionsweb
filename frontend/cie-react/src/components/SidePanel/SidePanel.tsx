import './SidePanel.css';
import { useParameters } from '../../context/parameter-context';
import { useEffect } from 'react';

export const SidePanel: React.FC = () => {
  const { htmlContent } = useParameters(); 

  useEffect(()=>{
    if( typeof window?.MathJax !== "undefined"){
      window.MathJax.typesetClear()
      window.MathJax.typeset()
    }
  },[htmlContent]) 
  

  return (
    
    <div className="sidePanel" dangerouslySetInnerHTML={{ __html: htmlContent }} />
  );
};