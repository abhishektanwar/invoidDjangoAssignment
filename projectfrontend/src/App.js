import React,{Component} from 'react';
import "./app.css";
class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      base64_str : null,
      md5:null,
      timestamp:null,
      AES_encrypted_timestamp:null
    };
  }

  handleFilesChosen = event => {
    this.setState({
        files: event.target.files[0]
    });
  }

  handleUploadClick = event => {
    event.preventDefault();
    let formDataa = new FormData();
    formDataa.append('files',this.state.files)
    fetch('http://localhost:8000/encodeimage/', {
        method: 'POST',
        body: formDataa,
    })
      .then(response => response.json())
      .then(data => this.setState({base64_str:data.base64_str,md5:data.md5,timestamp:data.timestamp,AES_encrypted_timestamp:data.AES_encrypted_timestamp}))
      .then(err => console.log(err));
}

  render() {
    const {tyu,base64_str,md5,AES_encrypted_timestamp,timestamp} = this.state;
    return (
      
      <div className="App" style={{margin:'10%'}}>
        <h1>Upload jpeg / jpg / png</h1>
        <form >

          <input
              type="file"
              multiple={false}
              accept=".jpg,.png,.jpeg"
              onChange={this.handleFilesChosen}
          />
          <input className='button' type="submit" onClick={this.handleUploadClick}/>
        </form>


        <div className='mainContainer'>
          <h3>{`${base64_str ?'Base 64':''}`}</h3>
          <div className={`${base64_str?'container':''}`}>{base64_str}</div>
          <h3>{`${base64_str ?'MD5':''}`}</h3>
          <div>{md5}</div>
          <h3>{`${base64_str ?'timestamp':''}`}</h3>
          <div>{timestamp}</div>
          <h3>{`${base64_str ?'AES encrypted timestamp':''}`}</h3>
          <div>{AES_encrypted_timestamp}</div>
        </div>
      </div>
    );
    }
  
}

export default App;
