import { useParameters } from "../../context/parameter-context";
import LoadingIndicator from "../LoadingIndicator";
import IframeComponent from "./IframeComponent";

/**
 * React functional component that renders an iframe from the given url.
 * Renders an IframeComponent from the '/sidemenu' endpoint of the backend API. 
 * Serves as the sidemenu component.
 * @returns {JSX.Element} Renders the LoadingIndicator during the fetching process.
 * Rendered sidemenu iframe component if sidemenu exists, otherwise returns null.
 */
const SideMenuIframe: React.FC = () => {
    const { sidemenuUrl, isLoading } = useParameters();

    if (isLoading) {
      return <LoadingIndicator />;
    }

    return (
      sidemenuUrl && <IframeComponent iframe_url={sidemenuUrl} />
      );
  };
  
  export default SideMenuIframe;