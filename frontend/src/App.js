import React from "react";
import {
  Button,
  Input,
  Form,
  Message,
  Card,
  Container,
  Segment,
  Grid,
  Header
} from 'semantic-ui-react'
import Layout from './components/Layout.js';
import Home from './components/Home.js';
import _Header from './components/Header.js';
import _Table from './components/Table.js';
import Deck from './components/Deck.js';
import DisplayData from './components/DisplayData.js';
import { Route, Routes } from "react-router-dom"

class App extends React.Component {
  state = {
    activeDataFormat: 'card', // table
    activeItem: 'home',
    payload: null,
    loading: false,
    timeout: 30,
    days: 0,

    // Error
    error: false,
    errorMessage: '',
    hidden: true,
  };

  handleActiveItem = async (e, { name }) => {
    await this.setState({ activeItem: name })
    console.log(`activeItem App:handleItem: ${this.state.activeItem}`);
  }

  expiring_in = async (e, value) => {
    e.preventDefault();
    console.log(`Searching with ${this.state.days} days`)
    const myHeaders = new Headers({
        'Content-Type': 'application/json',
        'X-Custom-Header': 'ProcessThisImmediately'
      });          
    // const response = await fetch(`http://127.0.0.1:5000/api/v1/expiringDomains?days=${this.state.days}`);
    const response = await fetch(`http://127.0.0.1:5000/api/v1/expiredDomains`, {headers: myHeaders});
    // const response = await fetch(`http://127.0.0.1:5000/api/v1/allDomains?order=asc`);
    const payload = await response.json();
    await this.setState({ payload });
    return payload;
  };

  dismissError = async (e, value) => {
    e.preventDefault();
    this.setState({ 
      hidden: false,
      error: true,
      errorMessage: ''
    });
    console.log(`activeItem App:dismissError: ${this.state.activeItem}`);
  };

  render() {
    const { activeItem } = this.state

    return (
      <Layout>
      <div className="App" id="App">
        <Grid >
          
          <Grid.Row columns={3}>
            <Grid.Column>
              <_Header handler={this.handleActiveItem}/>
            </Grid.Column>
            <Grid.Column>
            </Grid.Column>
            <Grid.Column>
            </Grid.Column>
          </Grid.Row>

          <Grid.Row>
            <Grid.Column>
              {
                this.state.activeItem === 'home' ? (<_Table />) : (null)
              }
              {
                this.state.activeItem === 'expiring' ? (<Home />) : (null)
              }
              {
                this.state.activeItem === 'all' ? (<_Table />) : (null)
              }
            </Grid.Column>
          </Grid.Row>

        </Grid>
      </div>
      </Layout>
    )
  }
}

export default App;


