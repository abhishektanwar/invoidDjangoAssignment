import React,{Component} from 'react';

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

}

  render() {
    const {tyu,base64_str,md5,AES_encrypted_timestamp,timestamp} = this.state;
    return (
      <div className="App">
        <form >

          <input
              type="file"
              multiple={false}
              accept=".jpg,.png,.jpeg"
              onChange={this.handleFilesChosen}
          />
          <input type="submit" onClick={this.handleUploadClick}/>
        </form>


        <div>{base64_str}</div>
        <div>{md5}</div>
        <div>{timestamp}</div>
        <div>{AES_encrypted_timestamp}</div>
      </div>
    );
    }
  
}

export default App;
