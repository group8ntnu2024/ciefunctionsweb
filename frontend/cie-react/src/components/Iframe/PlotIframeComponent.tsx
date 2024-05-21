import { useParameters } from "../../context/parameter-context";
import LoadingIndicator from "../LoadingIndicator";
import IframeComponent from "./IframeComponent";

/**
 * React functional component that renders an iframe from the given url.
 * Renders an IframeComponent from the '/plot' endpoint of the backend API. 
 * Serves as the plot component.
 * @returns {JSX.Element} Renders the LoadingIndicator during the fetching process.
 * Rendered plot iframe component if plotUrl exists, otherwise returns null.
 */
const PlotIframe: React.FC = () => {
    const { plotUrl, isLoading } = useParameters();

    if (isLoading) {
        return <LoadingIndicator />;
      }

    return (
        plotUrl && <IframeComponent iframe_url={plotUrl} />
    );
  };
  
  export default PlotIframe;