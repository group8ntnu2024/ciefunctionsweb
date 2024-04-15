import '../app-content.css';
import PlotlyPlot from './plotly-plot';

function PlotContent() {
  return (
    <div className="content-container row">
      <div className="graphic col-md-9">
      <>
        <PlotlyPlot />
      </>
    </div> 
  </div> 
  );
}

export default PlotContent;
