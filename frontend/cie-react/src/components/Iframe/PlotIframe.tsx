import { useParameters } from "../../context/parameter-context";
import IframeComponent from "./IframeComponent";

const PlotIframe: React.FC = () => {
    const { plotUrl } = useParameters();

    return (
        plotUrl && <IframeComponent iframe_url={plotUrl} />
    );
  };
  
  export default PlotIframe;