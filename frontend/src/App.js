import React from "react";
import {
  Button,
  // Input,
  // Form,
  // Message,
  // Card,
  // Container,
  // Segment,
  Grid,
  // Header
} from 'semantic-ui-react'
import Layout from './components/Layout.js';
import Expiring from './components/Expiring.js';
import _Header from './components/Header.js';
import _Table from './components/Table.js';
import BulkSearch from './components/BulkSearch';
// import { Route, Routes } from "react-router-dom"


import Onboard from '@web3-onboard/core'
import injectedModule from '@web3-onboard/injected-wallets'

const injected = injectedModule()

const wallets = [injected]

const chains = [
    {
      id: 1,
      token: 'ETH',
      label: 'Ethereum Mainnet',
      rpcUrl: 'http://geth.dappnode:8545'
    },
    {
      id: 137,
      token: 'MATIC',
      label: 'Matic Mainnet',
      rpcUrl: 'https://matic-mainnet.chainstacklabs.com'
    }
  ]

  const appMetadata = {
    name: 'My App',
    icon: '<SVG_ICON_STRING>',
    logo: '<SVG_LOGO_STRING>',
    description: 'My app using Onboard',
    recommendedInjectedWallets: [
      { name: 'Coinbase', url: 'https://wallet.coinbase.com/' },
      { name: 'MetaMask', url: 'https://metamask.io' }
    ]
  }

const onboard = Onboard({
    wallets,
    chains,
    appMetadata
  })

// const connectedWallets = await onboard.connectWallet()



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


  siwe = async (e, value) => {
    e.preventDefault();
    await onboard.connectWallet()
    // this.setState({ 
    //   hidden: false,
    //   error: true,
    //   errorMessage: ''
    // });
    console.log(`activeItem App:dismissError: ${this.state.activeItem}`);
  };

  render() {
    // const { activeItem } = this.state

    return (
      <Layout>
      <div className="App" id="App">
        <_Header handler={this.handleActiveItem}/>

        <div class="ui hidden section divider"></div>
        <div class="ui hidden section divider"></div>

        <Button onClick={this.siwe}
          className="icon"
          labelPosition='left'>
          All Expired domains
        </Button>

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


