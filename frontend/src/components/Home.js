import React, { Component } from 'react'
import { Input, Menu, Button, Card, Container } from 'semantic-ui-react'
import { NavLink, withRouter } from 'react-router-dom'
import Deck from './Deck.js'

export default class Home extends Component {
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
        console.log(`activeItem: ${this.state.activeItem}`);
        // console.log(`Days: ${this.state.days}`);
        // console.log(`payload: ${JSON.stringify(this.state.payload)}`);
        // console.log(`error message: ${this.state.errorMessage}`);
        // console.log(`hidden: ${this.state.hidden}`);
      };
    

  render() {
    return (
    <div className="Home" id="home">
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
    
    < div style = {{margin: 100}}>
    <Container>
        <div>
        <Card.Group itemsPerRow="4" textAlign="center" className='domains'>
            {this.state.payload == null ? (<div>Load data...</div>) : 
            (
                this.state.payload.expiring_domains.map(domain => 
                    // console.log(`WORKING?: ${JSON.stringify(domain)}`)
                    <Deck payload={domain}/>
                )
            )
            }
        </Card.Group>
        </div>
    </Container>
    </div>
    </div>
    )
  }
}