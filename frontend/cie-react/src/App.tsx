import { createHashRouter, Navigate, Outlet, RouterProvider } from "react-router-dom";
import Navbar from "./components/navbar/navbar";
import { PLOT_ROUTE, TABLE_ROUTE } from "./utils/router-urls";
import PlotContent from "./components/plot/plot-content";
import TableContent from "./components/table/table-content";
import ParametersLayout from "./components/parameters/parameters-layout";
import { PulldownMenu } from "./components/PulldownMenu/PulldownMenu";
import { SidePanel } from "./components/SidePanel/SidePanel";
import { ParametersProvider } from './context/parameter-context';
import { UseContentControllerProvider } from "./hooks/useContentController";
import { PlotTypeProvider } from "./context/PlotTypeContext";

function App() {
  const router = createHashRouter([
    {
      path: "/",
      element: (
        <UseContentControllerProvider>
        <ParametersProvider>
          <PlotTypeProvider>
            <div className="outer-container">
              <Navbar />
              <div className="inner-container">
                <div className="plo">
                  <Outlet />
                  <PulldownMenu />
                </div>
                <div className="sid">
                  <SidePanel />
                </div>
              </div>
            </div>
          </PlotTypeProvider>
        </ParametersProvider>
      </UseContentControllerProvider>
      ),
      children: [
        { path: "", element: <Navigate to={PLOT_ROUTE} replace /> },
        { path: PLOT_ROUTE, element: <ParametersLayout><PlotContent/></ParametersLayout> },
        { path: TABLE_ROUTE, element: <ParametersLayout><TableContent/></ParametersLayout> },
      ],
    }
  ]);

  return <RouterProvider router={router} />;
}

export default App;
