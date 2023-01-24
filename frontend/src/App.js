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
import { ethers } from 'ethers'

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


class App extends React.Component {
  state = {
    activeDataFormat: 'card', // table
    activeItem: 'home',
    payload: null,
    loading: false,
    timeout: 30,
    days: 0,
    connectedWallet: null,

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
    const connectedWallet = await onboard.connectWallet()

    if (connectedWallet[0]) {
      // create an ethers provider with the last connected wallet provider
      const ethersProvider = await new ethers.providers.Web3Provider(
        connectedWallet[0].provider,
        'any'
      )
      let bal = await ethersProvider.getBalance(connectedWallet[0].accounts[0].address)
      console.log(`Connected Address Balance: ${bal}`)
      debugger
      const signer = await ethersProvider.getSigner()
      const msg = await signer.signMessage('Message')
      console.log('Hold here to inspect debugger insight')
    }
    await this.setState({ connectedWallet })
    console.log(`Connected Address: ${connectedWallet[0].accounts[0].address}`)
    console.log(`Connected ENS Name: ${connectedWallet[0].accounts[0].ens.name}`)
    console.log(`ConnectedWallets: ${connectedWallet}`);
  };

  disconnect = async (e, value) => {
    e.preventDefault();
    debugger
    const disconnected = await onboard.disconnectWallet(this.state.connectedWallet)
    console.log(`disconnected: ${disconnected}`);
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
          SIWE
        </Button>
        <Button onClick={this.disconnect}
          className="icon"
          labelPosition='left'>
          Disconnect SIWE
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


