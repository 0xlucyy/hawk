import React from "react";
import {
  Button,
  Input,
  Form,
  Message,
  Card,
  Container,
  Segment,
  Grid
} from 'semantic-ui-react'
import Layout from './components/Layout.js';
import Home from './components/Home.js';
import Header from './components/Header.js';
import Deck from './components/Deck.js';
import Contact from './components/Contact.js';
import DisplayData from './components/DisplayData.js';
import { Route, Routes } from "react-router-dom"

class App extends React.Component {
  state = {
    activeItem: 'home',
    payload: null,
    loading: false,
    timeout: 30,
    days: 0,
    error: false,
    errorMessage: '',
    hidden: true,
  };

  handleActiveItem = async (e, { name }) => {
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
      <Segment inverted vertical style={{ margin: '20em 0em 0em', padding: '5em 0em' }}>
        <Container className="App" id="App" textAlign="center">
          <Layout>
            <Grid divided inverted stackable>
              <Grid.Column width={4}>
                <Header handler={this.handleActiveItem}/>
              </Grid.Column>
              <Grid.Column width={12}>
                {
                  this.state.activeItem === 'home' ? (<Home />) : (null)
                }
                {
                  this.state.activeItem === 'expiring' ? (<DisplayData />) : (null)
                }
              </Grid.Column>
            </Grid>
          </Layout>
        </Container>
      </Segment>
    )
  }
}

export default App;


{/* <Input 
placeholder="activeItem"
onChange={ (event) => {
    this.setState({ activeItem: event.target.value });
}}
>
</Input>
<Button onClick={this.dismissError}
className="icon"
labelPosition='left'>
dismissError!
</Button> */}