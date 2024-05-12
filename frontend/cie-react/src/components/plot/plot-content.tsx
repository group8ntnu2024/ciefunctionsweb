
import { useContentController } from '../../hooks/useContentController.tsx';
import ThreeLineDiagram from './ThreeLineDiagram.tsx';
import MacLeodBoyntonChromaticityDiagram from './MacLeodBoyntonChromaticityDiagram.tsx';
import MaxwellianlmChromaticityDiagram from './MaxwellianlmChromaticityDiagram.tsx';
import XyConeFundamentalBasedChromaticityDiagram from './XyConeFundamentalBasedChromaticityDiagram.tsx';
import XyStandardChromaticityDiagram from './XyStandardChromaticityDiagram.tsx';
import XyConeFundamentalBasedChromaticityDiagramPls from './XyConeFundamentalBasedChromaticityDiagramPls.tsx';


const methodComponents: { [key: string]: React.ComponentType } = {
  method1: ThreeLineDiagram, //correct
 
  method2: ThreeLineDiagram, //correct

  method3: MacLeodBoyntonChromaticityDiagram, //correct

  method4: MaxwellianlmChromaticityDiagram, //correct

  method5: ThreeLineDiagram, //correct

  method6: XyConeFundamentalBasedChromaticityDiagram, //correct

  method7: ThreeLineDiagram, //correct
  
  method8: XyConeFundamentalBasedChromaticityDiagramPls, //wrong

  method9: ThreeLineDiagram, //correct

  method10: XyStandardChromaticityDiagram, //correct
};

const PlotContent: React.FC = () => {
  const { selectedOption } = useContentController();

  const PlotComponent = methodComponents[selectedOption] || ThreeLineDiagram;

  return (
    <div>
      <PlotComponent />
    </div>
  );
};

export default PlotContent;