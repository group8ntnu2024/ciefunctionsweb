import { useScreenWidth } from '../hooks/useScreenWidth';
import SideMenuIframe from '../components/Iframe/SideMenuIframe';

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