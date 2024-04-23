
import { useContentController } from '../../hooks/useContentController.tsx';
import ThreeLineDiagram from './ThreeLineDiagram.tsx';
import ChromaticityDiagram1 from './ChromaticityDiagram1.tsx';
import ChromaticityDiagram2 from './ChromaticityDiagram2.tsx';
import ChromaticityDiagram3 from './ChromaticityDiagram3.tsx';


const methodComponents: { [key: string]: React.ComponentType } = {
  method1: ThreeLineDiagram, //correct
 
  method2: ThreeLineDiagram, //correct

  method3: ChromaticityDiagram2, //correct

  method4: ChromaticityDiagram1, //correct

  method5: ThreeLineDiagram, //correct

  method6: ChromaticityDiagram1, //correct

  method7: ThreeLineDiagram, //correct
  
  method8: ChromaticityDiagram3, //wrong

  method9: ThreeLineDiagram, //correct

  method10: ChromaticityDiagram1, //correct
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