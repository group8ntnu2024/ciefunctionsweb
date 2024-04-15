import { useState } from "react";

import { createHashRouter, Outlet, RouterProvider } from "react-router-dom";
import Navbar from "./components/navbar/navbar";
import { PLOT_ROUTE, TABLE_ROUTE } from "./utils/router-urls";
import PlotContent from "./components/plot/plot-content";
import TableContent from "./components/table/table-content";
import ParametersLayout from "./components/parameters/parameters-layout";
import { PulldownMenu } from "./components/PulldownMenu/PulldownMenu";
import { SidePanel } from "./components/SidePanel/SidePanel";
import { ParametersProvider } from './context/parameter-context';
import './index.css';
import './components/app-content.css';

function App() {
  const [selectedOption, setSelectedOption] = useState("method1");

  const router = createHashRouter([
    {
      path: "/",
      element: 
<div className="container">
    <Navbar/>
    <div className="row">
        <div className="col-md-9">
            <Outlet />
            <div>
                <PulldownMenu onChange={setSelectedOption} />
            </div>
        </div>
        <div className="col-md-3">
            <SidePanel selectedOption={selectedOption} />
        </div>
    </div>
</div>
,

      children: [
        { path: PLOT_ROUTE, element: <ParametersLayout><PlotContent/></ParametersLayout> },
        { path: TABLE_ROUTE, element: <ParametersLayout><TableContent/></ParametersLayout> },
      ],
    }
  ]);

  return (
    <ParametersProvider>
      <RouterProvider router={router} />
    </ParametersProvider>
  );
}

export default App;





