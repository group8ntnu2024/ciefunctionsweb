import { useScreenWidth } from '../hooks/useScreenWidth';
import SideMenuIframe from '../components/Iframe/SideMenuIframeComponent';

/**
 * Function for rendering the sidemenu when it is to be placed to the right of the plot/table
 * @returns  {JSX.Element} The rendered sidemenu iframe if the screen width is less than or equal to 1200px.
 */
export const renderRightGridInformationIframe = () => {
  const screenWidth = useScreenWidth();
  return (
    <>
      {screenWidth <= 1200 && (
        <div className="sid">
          <SideMenuIframe />
        </div>
      )}
    </>
  );
};

/**
 * Function for rendering the sidemenu when it is to be placed to the right of the plot/table
 * @returns  {JSX.Element} The rendered sidemenu iframe if the screen width is more than 1200px.
 */
export const renderBottomGridInformationIframe = () => {
  const screenWidth = useScreenWidth();
  return (
    <>
      {screenWidth > 1200 && (
        <div className="sid">
          <SideMenuIframe />
        </div>
      )}
    </>
  );
};