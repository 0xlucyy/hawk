import React from "react";
// import axios from 'axios';
import {Button, Input, Form, Message, Card, Container} from 'semantic-ui-react'
import Layout from './components/Layout.js';
import Deck from './components/Deck.js';
import Display from './components/Display.js';
import Test from './components/Test.js';

class App extends React.Component {
  state = {
    payload: null,
    loading: false,
    timeout: 30,
    days: 0,

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  expiring_in = async (e, value) => {
    e.preventDefault();
    console.log(`Searching with ${this.state.days} days`)
    const response = await fetch(`http://127.0.0.1:5000/api/v1/expiring?days=${this.state.days}`);
    const payload = await response.json();
    this.setState({ payload });
    // console.log(payload);
    return payload;
  };

  handleDismiss = async (e, value) => {
    e.preventDefault();
    console.log(`handleDismiss`);
    await this.setState({ 
      hidden: false,
      error: true,
      errorMessage: ''
    });
    // console.log(`Days: ${this.state.days}`);
    // console.log(`payload: ${JSON.stringify(this.state.payload)}`);
    // console.log(`error message: ${this.state.errorMessage}`);
    // console.log(`hidden: ${this.state.hidden}`);
  };

  render() {
    // const listItems = this.state.payload.expiring_domains.map((domain) => <li key={domain.name}>{domain.name}</li>);
    return (
      <Layout>
        <div style = {{margin: 100}}>
          <h2 style = {{color: "green"}}> ENS Hawk </h2>

          <Input 
            placeholder="Days"
            onChange={ (event) => {
              this.setState({ days: event.target.value });
            }}
          >
          </Input>
          <Button onClick={this.expiring_in}
                  className="icon"
                  labelPosition='left'>
                  expiring_in!
          </Button>
          <Button onClick={this.handleDismiss}
                  className="icon"
                  labelPosition='left'>
                  handleDismiss!
          </Button>
        </div>
          
        < div style = {{margin: 100}}>
        <Container>
          <Card.Group stackable itemsPerRow={3}>
            <div>
              {this.state.payload == null ? (<div>Load data...</div>) : 
                (
                  this.state.payload.expiring_domains.map(domain => 
                    // console.log(`WORKING?: ${JSON.stringify(domain)}`)
                    <Deck payload={domain}/>
                  )

                ) 
              }
            </div>
          </Card.Group>
        </Container>
        </div>
      </Layout>
    )
  }
}

export default App;
