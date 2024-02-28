import {createHashRouter, Outlet, RouteObject, RouterProvider} from "react-router-dom";
import Navbar from "./components/navbar/navbar";
import { PLOT_ROUTE, TABLE_ROUTE } from "./utils/router-urls";
import PlotContent from "./components/plot/plot-content";
import TableContent from "./components/table/table-content";
import { ParametersProvider } from './context/parameter-context';
import Layout from "./components/parameters/parameters-layout";

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
                element: <Layout><PlotContent/></Layout>,
            },
            {
                path: TABLE_ROUTE,
                element: <Layout><TableContent/></Layout>,
            }
        ]
        
    }
]

const Router = () => {
    return <RouterProvider router={createHashRouter(routes)}/>;
};


function App() {
    return (
        <ParametersProvider>
            <Router/>
        </ParametersProvider>
    );
}

export default App;