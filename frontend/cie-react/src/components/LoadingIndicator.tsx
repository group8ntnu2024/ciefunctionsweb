
/**
 * Layout for loading indicator.
 * Designed to be modular and reusable for components across the application.
 */
const LoadingIndicator: React.FC = () => {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100%',
      fontSize: '20px'
    }}>
      Loading...
    </div>
  );
};

export default LoadingIndicator;