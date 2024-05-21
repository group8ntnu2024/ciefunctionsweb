import { createHashRouter, Navigate, Outlet, RouterProvider } from "react-router-dom";
import Navbar from "./components/navbar/NavbarComponent.tsx";
import { PLOT_ROUTE, TABLE_ROUTE } from "./utils/router-urls.tsx";
import TableContent from "./components/table/TableComponent.tsx";
import ParametersLayout from "./components/parameters/ParametersLayoutComponent.tsx";
import { ParametersProvider } from './context/parameter-context.tsx';
import { UseContentControllerProvider } from "./hooks/useContentController.tsx";
import PlotIframe from "./components/Iframe/PlotIframeComponent.tsx";
import { renderRightGridInformationIframe, renderBottomGridInformationIframe } from "./utils/side-menu-iframe-util.tsx";

/**
 * Application component that sets up routing, context providers.
 *  
 * @returns {JSX.Element} The application component with routing and context providers.
 */
function App() {
  
  const router = createHashRouter([
    {
      path: "/",
      element: (
        <UseContentControllerProvider>
          <ParametersProvider>
            <Navbar />
            <div className="outer-container">
              <Outlet />
            </div>
          </ParametersProvider>
        </UseContentControllerProvider>
      ),
      children: [
        { path: "", element: <Navigate to={PLOT_ROUTE} replace /> },
        { path: PLOT_ROUTE, element: <div className="inner-container">
        <div className="plo">
          <ParametersLayout><PlotIframe/></ParametersLayout>
          {renderRightGridInformationIframe()}
        </div>
        {renderBottomGridInformationIframe()}
        </div> },
        { path: TABLE_ROUTE, element: <div className="inner-container">
        <div className="tab">
          <ParametersLayout><TableContent/></ParametersLayout>
          {renderRightGridInformationIframe()}
        </div>
        {renderBottomGridInformationIframe()}
      </div> },
      ],
    }
  ]);

  return <RouterProvider router={router} />;
}

export default App;
