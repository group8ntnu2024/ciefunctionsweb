
import { Link } from 'react-router-dom';
import './navbar.css'
import { PLOT_ROUTE, TABLE_ROUTE } from '../../utils/router-urls';

/**
 * React functional component that renders a navigation bar using react-router-dom.
 * Provides links to routes to the application: plot and table. When clicked this routes to the respective
 * component that the user wants to display.
 * @returns {JSX.Element} Navbar component as a JSX element
 */
const Navbar = () => {
    return (
        <nav className="navbar">
            <ul className="navbar-list">
                <li className="navbar-item"><Link to={PLOT_ROUTE}>Plot</Link></li>
                <li className="navbar-item"><Link to={TABLE_ROUTE}>Table</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;