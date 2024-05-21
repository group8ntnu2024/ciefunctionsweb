import { useEffect, useState } from 'react';
import '../index.css'

/**
 * Hook for determening the width of the browser window. Can be used to 
 * manage view conditions in the applicaiton.
 * @returns {number} The current width of the browser window.
 */
export const useScreenWidth = () => {
  const [screenWidth, setScreenWidth] = useState(window.innerWidth);
  useEffect(() => {
    const handleResize = () => {
      setScreenWidth(window.innerWidth);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return screenWidth;
};
