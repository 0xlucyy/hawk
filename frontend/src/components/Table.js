import React from "react";
// import axios from 'axios';
// import {Button, Input, Form, Message, Card, Container} from 'semantic-ui-react'
// import Layout from './components/Layout.js';
// import Deck from './components/Deck.js';
// import Display from './components/Display.js';
// import Test from './components/Test.js';

class Table extends React.Component {
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


  render() {
    // const listItems = this.state.payload.expiring_domains.map((domain) => <li key={domain.name}>{domain.name}</li>);
    return (
        <div style = {{margin: 100}}>
          <h2 style = {{color: "green"}}> NEW PAGE </h2>
        </div>
    )
  }
}

export default Table;
