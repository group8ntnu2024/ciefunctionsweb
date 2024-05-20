
import { Link } from 'react-router-dom';
import './navbar.css'
import { PLOT_ROUTE, TABLE_ROUTE } from '../../utils/router-urls';

/**
 * 
 * @returns 
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