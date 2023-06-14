const ProgressBar = ({ completed }) => {
    
    const containerCss = {
      height: 23,
      width: '100%',
      backgroundColor: "#e0e0de",
      borderRadius: 50,
      margin: 30
    }
  
    const fillerCss = {
      height: '100%',
      width: `${completed}%`,
      backgroundColor: "#42bbbb",
      borderRadius: 'inherit',
      textAlign: 'right',
      overflow: 'hidden'
    }
  
    const labelCss = {
      padding: 5,
      color: 'white',
      fontWeight: 'bold',
    }
  
    return (
      <div style={containerCss}>
        <div style={fillerCss}>
          <span style={labelCss}>{`${completed > 10.0 ? completed+'%' : ''}`}</span>
        </div>
      </div>
    );
};
  
export default ProgressBar;