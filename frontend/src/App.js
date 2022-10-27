import React from "react";
import {Button, Input, Form, Message, Card, Container} from 'semantic-ui-react'
import Layout from './components/Layout.js';
import Home from './components/Home.js';
import Deck from './components/Deck.js';
import { Route, Routes } from "react-router-dom"

class App extends React.Component {
  state = {
    activeItem: 'home',

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  handleItemClick = (e, { name }) => {
    this.setState({ activeItem: name })
  }

  dismiss = async (e, value) => {
    e.preventDefault();
    console.log(`activeItem: ${this.state.activeItem}`);
    this.setState({ 
      hidden: false,
      error: true,
      errorMessage: ''
    });
  };

  render() {
    // const listItems = this.state.payload.expiring_domains.map((domain) => <li key={domain.name}>{domain.name}</li>);
    const { activeItem } = this.state

    return (
      <div className="App" style = {{margin: 100}}>
        <Layout>
          <Button onClick={this.dismiss}
            className="icon"
            labelPosition='left'>
            dismiss!
          </Button>
          <Home />
        </Layout>
      </div>
    )
  }
}

export default App;
