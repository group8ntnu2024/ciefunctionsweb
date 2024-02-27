import {createHashRouter, Outlet, RouteObject, RouterProvider} from "react-router-dom";
import Navbar from "./components/navbar/navbar";
import { PLOT_ROUTE, TABLE_ROUTE } from "./utils/router-urls";
import PlotContent from "./components/plot-content";
import TableContent from "./components/table-content";

const routes: RouteObject[] = [
    {
        path: "/",
        element: (
            <div>
                <Navbar/>
               <Outlet />
            </div>
            
               
        ),
        children: [
            {
                path: PLOT_ROUTE,
                element: <PlotContent/>,
            },
            {
                path: TABLE_ROUTE,
                element: <TableContent/>
            }
        ]
        
    }
]

const Router = () => {
    return <RouterProvider router={createHashRouter(routes)}/>;
};


function App() {
    return (
        <Router />
    );
}

export default App;