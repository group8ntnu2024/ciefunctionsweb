import React from 'react';

type IframeProps = {
  iframe_url: string;
};


const IframeComponent: React.FC<IframeProps> = ({ iframe_url }) => {
  return (
    <iframe
      src={iframe_url}
      style={{ width: '1000px', height: '875px', border: 'none' }}
      title="iframe-component"
      allowFullScreen
    ></iframe>
  );
};

export default IframeComponent;