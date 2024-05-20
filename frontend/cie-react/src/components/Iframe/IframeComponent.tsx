import React from 'react';

/**
 * Prop for IframeComponent
 * @property {string} iframe_url The url from where the iframe is
 * fetched from the backend API.
 */
type IframeProps = {
  iframe_url: string;
};

/**
 * React functional component that renders and iframe from the given url.
 * Provides 
 * @param {IframeProps} props The props for the component
 * @returns {JSX.Element} Rendered iframe component.
 */
const IframeComponent: React.FC<IframeProps> = ({ iframe_url }) => {
  return (
    <iframe
      src={iframe_url}
      style={{ width: '100%', height: '100%', border: 'none'}}
      title="iframe-component"
      allowFullScreen
    ></iframe>
  );
};

export default IframeComponent;