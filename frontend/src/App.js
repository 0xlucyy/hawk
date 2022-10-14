// import React, {useState, useEffect} from "react";

// function App() {

//   const [data, setData] = useState(null)

  // useEffect(() => {
  //   fetch("http://127.0.0.1:5000/api/v1/expiring?days=6")
  //     .then(res => res.json())
  //     .then(data => {
  //       setData(data)
  //       console.log(data)
  //     })
  //     .catch((err) => {
  //       console.log(err.message);
  //     })
  //   }, []
  // )

//   return (
//     <div>
//       <h3>Total expiring: {data.total_expiring}.</h3>
//       <h3>Expiring within: {data.expiring_within} days.</h3>

//       {/* {
//         data.expiring_domains.map((domain) => (
//         <ol key = { domain.id }>
//           Name: { domain.name },
//           Hash: { domain.hash }, 
//           Expiration: { domain.expiration } 
//         </ol>
//         ))
//       } */}
//     </div>
//   )
// }

// export default App


import React, {useState, useEffect} from "react";
import {Button} from 'semantic-ui-react'
  
class App extends React.Component {

  state = {
    payload: null,
    isLoaded: false,
    error: false
  };

  call() {
    alert("Welcome to GFG");
  }

  setData = (data) => {
    this.setState({ payload: data })
  }

  get_some_data = () => {
    fetch("http://127.0.0.1:5000/api/v1/expiring?days=6")
    .then(res => res.json())
    .then(data => {
      this.setData(data)
      console.log(this.state.payload)
    })
    .catch((err) => {
      console.log(err.message);
    })
  }
  
  render() {
    return (
      < div style = {{margin: 100}}>
      {/* {this.get_some_data()} */}
      <h2 style = {{color: "green"}}> GeeksforGeeks </h2>
      <b><p> Semantic UI React Integration </p></b>
      <hr/> <br/>< strong > Alert button: </strong>
      <br/> < br />
      <Button onClick={this.get_some_data}
              className="icon"
              labelPosition='right'>
              Click here!
      </Button> 
      </div>
    );
  }
}

export default App;
