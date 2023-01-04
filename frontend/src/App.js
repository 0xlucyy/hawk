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
import Expiring from './components/Expiring.js';
import _Header from './components/Header.js';
import _Table from './components/Table.js';
import BulkSearch from './components/BulkSearch';
// import { Route, Routes } from "react-router-dom"

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

  // This links Header.js to this.state.activeItem by
  // passing this function as a handler variable to
  // _Header component.
  handleActiveItem = async (e, { name }) => {
    e.preventDefault();
    await this.setState({ activeItem: name })
    console.log(`activeItem App:handleItem: ${this.state.activeItem}`);
  }


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
        <_Header handler={this.handleActiveItem}/>

        <div class="ui hidden section divider"></div>
        <div class="ui hidden section divider"></div>

        <Grid >
          <Grid.Row>
            <Grid.Column>
              {
                this.state.activeItem === 'home' ? (<Expiring />) : (null)
              }
              {
                this.state.activeItem === 'expiring' ? (<Expiring />) : (null)
              }
              {
                this.state.activeItem === 'all' ? (<_Table />) : (null)
              }
              {
                this.state.activeItem === 'bulk search' ? (<BulkSearch />) : (null)
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


