import React from "react";
import Layout from './components/Layout.js';
import Expiring from './components/Expiring.js';
import _Header from './components/Header.js';
import _Table from './components/Table.js';
import BulkSearch from './components/BulkSearch';
import {
  connectWeb3Wallet,
  createSignVerifyMessage,
} from './utils.js'
import {
  Button,
  Grid,
} from 'semantic-ui-react'


class App extends React.Component {
  state = {
    activeDataFormat: 'card', // table
    activeItem: 'bulk search',
    payload: null,
    loading: false,
    timeout: 30,
    days: 0,
    connectedWallet: null,
    EIP4361Message: null,

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
    
    // Attempt to connect to an ethereum wallet.
    const results = await connectWeb3Wallet();
    const ethersProvider = await results[0],
          connectedWallet = await results[1];

    if (connectedWallet[0] != false) {
      const verified_address = await createSignVerifyMessage(
        connectedWallet,
        ethersProvider
      )

      // debugger
  
      if (verified_address == false) {
        console.log("verified: FALSE");
      }
      else {
        console.log("verified: ", verified_address);
      }
    }

    await this.setState({ connectedWallet })
    // debugger
    console.log(`Connected Address: ${connectedWallet[0].accounts[0].address}`)
    console.log(`Connected ENS Name: ${connectedWallet[0].accounts[0].ens.name}`)
    console.log(`ConnectedWallets: ${connectedWallet}`);
  };

  // load_sig_data = async (address) => {
  //   console.log(`[ACTION] Loading reverse records data ...`)
  //   const params = new URLSearchParams();
  //   params.append('address', address);

  //   const response = await fetch('http://127.0.0.1:5000/api/v1/siwe', {
  //     method: 'POST',
  //     body: params
  //   });
  //   const data = await response.json();
  //   await this.setState({ EIP4361Message: data });
  //   console.log(`[ACTION] EIP4361 ...`)
  //   console.log(`Data: ${JSON.stringify(data)}`)
  // }

  disconnect = async (e, value) => {
    e.preventDefault();
    // debugger
    // const disconnected = await onboard.disconnectWallet(this.state.connectedWallet)
    // console.log(`disconnected: ${disconnected}`);
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
