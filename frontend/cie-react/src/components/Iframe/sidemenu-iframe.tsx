import { useParameters } from "../../context/parameter-context";
import IframeComponent from "./iframe-component";

const SideMenuIframe: React.FC = () => {
    const { sidemenuUrl } = useParameters();


    return (
        <div>
          {sidemenuUrl && <IframeComponent iframe_url={sidemenuUrl} />}
        </div>
      );
  };
  
  export default SideMenuIframe;