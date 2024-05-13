import { useParameters } from "../../context/parameter-context";
import IframeComponent from "./iframe-component";

const PlotIframe: React.FC = () => {
    const { plotUrl } = useParameters();

    return (
      <div>
        {plotUrl && <IframeComponent iframe_url={plotUrl} />}
      </div>
    );
  };
  
  export default PlotIframe;