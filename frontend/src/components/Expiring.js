import React, { Component, useEffect, useState } from 'react'
import { Input, Menu, Button, Card, Container, Image, Popup, Progress } from 'semantic-ui-react'
import {_Card, HandleCardContext} from './Card.js'
import {
  handleReverseRecord}
from "../utils.js"
// console.log(`data: ${JSON.stringify(markets)}`)

var async = require("async");


export default class Expiring extends Component {
  state = {
    expiringin_payload: null,
    expired_payload: null,
    markets: null,
    loading: false,
    timeout: 30,
    days: null,
    view: 'card',
    premium: null,
    rates: null,
    reverse_records: null,
    days_until_expire_button_loading: false,
    expired_button_loading: false,

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  load_market_data = async () => {
    if (this.state.markets === null) {
      console.log(`Loading market data....`)
      let response = await fetch(`http://127.0.0.1:5000/api/v1/allMarkets?order=asc`);
      const markets = await response.json();
      await this.setState({ markets });
    }
  }

  load_rr = async (addresses) => {
    const params = new URLSearchParams();
    params.append('addresses', addresses);

    const response = await fetch('http://127.0.0.1:5000/api/v1/getReverseRecords', {method: 'POST', body: params});
    const data = await response.json();
    console.log(`Data: ${JSON.stringify(data)}`)
    console.log(`reverse_records: ${JSON.stringify(data.reverse_records)}`)
    console.log(`LookUp: ${JSON.stringify(data.reverse_records['0xE2FaA63f2351c6F2b88659f2fFfC2167172D329a'])}`)
    await this.setState({ reverse_records: data });
  }

  load_rates_data = async () => {
    if (this.state.rates == null) {
      console.log(`Loading rates data from coinbase....`)
      let response = await fetch(`https://api.coinbase.com/v2/exchange-rates?currency=ETH`);
      const rates = await response.json();
      await this.setState({ rates });
      // console.log(`Loaded Rates Data: ${JSON.stringify(rates)}`)
    }
  }

  expired = async (e, value) => {
    e.preventDefault();
    await this.setState({ expired_button_loading: true})

    await this.load_market_data()
    await this.load_rates_data()

    console.log(`Loading expired domain data....`)
    // let response = await fetch(`http://127.0.0.1:5000/api/v1/expiredDomains`);
    let response = await fetch('http://127.0.0.1:5000/api/v1/liveAuction');
    const expired_payload = await response.json();

    let owners = '';
    async.forEachOf(expired_payload.domains, (value, key, callback) => {
      // console.log(`v: ${JSON.stringify(value)}`)
      // console.log(`k: ${JSON.stringify(key)}`)
      if (value.owner !== undefined && value.owner !== null) {
        owners += value.owner + ','
      }
      callback();
    }, err => { if (err) console.error(err.message);}
    );
    console.log(`owners: ${owners}`)

    await this.load_rr(owners)
    await this.setState({ expiringin_payload: null });
    await this.setState({ expired_payload });
    await this.setState({ expired_button_loading: false})
  };

  expiring_in = async (e, value) => {
    e.preventDefault();

    await this.setState({ days_until_expire_button_loading: true})

    if (this.state.days === null) {
      this.setState({ days: 3 });
    }
    await this.load_market_data()
    await this.load_rates_data()

    console.log(`Loading expiring domains within ${this.state.days} days....`)
    let response = await fetch(`http://127.0.0.1:5000/api/v1/expiringDomains?days=${this.state.days}`);
    const expiringin_payload = await response.json();

    let owners = '';
    // https://github.com/caolan/async#each
    async.forEachOf(expiringin_payload.domains, (value, key, callback) => {
      if (value.owner !== undefined && value.owner !== null) {
        owners += value.owner + ','
      }
      callback();
    }, err => { if (err) console.error(err.message);}
    );
    console.log(`owners: ${owners}`)

    await this.load_rr(owners)
    await this.setState({ expired_payload: null });
    await this.setState({ expiringin_payload });
    await this.setState({ days_until_expire_button_loading: false})
  };

  handleDismiss = async (e, value) => {
    e.preventDefault();
    console.log(`handleDismiss`);
    await this.setState({
      hidden: false,
      error: true,
      errorMessage: ''
    });
  };

  test = () => {
    console.log(this.state.reverse_records)
  };


  render() {
    return (
    <div className="Home" id="home">

    <Input 
      error={this.state.error}
      placeholder="days"
      value={this.state.days}
      onChange={ (event) => {
          this.setState({ days: event.target.value });
    }}
    >
    </Input>
    <Button onClick={this.expiring_in}
            className="icon"
            labelPosition='left'
            loading={this.state.days_until_expire_button_loading}>
            Days until expiration
    </Button>
    <Button onClick={this.expired}
            className="icon"
            labelPosition='left'
            loading={this.state.expired_button_loading}>
            All Expired domains
    </Button>

    <Button onClick={this.test}
            className="icon"
            labelPosition='left'>
            Days until expiration
    </Button>
    < div style = {{marginTop: 100}}>
    <Container>
        <div>
        <Card.Group itemsPerRow="5" textAlign="center" className='domains'>
            {this.state.expired_payload == null ? (<div></div>) : 
            (
              this.state.expired_payload.domains.map(domain => (
                <Card centered fluid>
                  <Card.Content extra>
                  <div className='ui four buttons' id='card_header'>
                  <Popup
                    inverted
                    on='hover'
                    position='top center'
                    size='small'
                    content='Opensea'
                    trigger={<Image
                        src='./opensea.png'
                        as='a'
                        size='small'
                        href={this.state.markets.markets.opensea.base_url + '/assets/ethereum/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
                        target='_blank'
                        circular
                    />}
                  />
                  <Popup
                    inverted
                    on='hover'
                    position='top center'
                    size='small'
                    content='ENS Vision'
                    trigger={<Image
                        src='./ensvision.jpg'
                        as='a'
                        size='small'
                        href={this.state.markets.markets.ensvision.base_url + '/name/' + domain.name}
                        target='_blank'
                        circular
                    />}
                  />
                  <Popup
                    inverted
                    on='hover'
                    position='top center'
                    size='small'
                    content='LooksRare'
                    trigger={<Image
                        src='./looksrare.jpg'
                        as='a'
                        size='small'
                        href={this.state.markets.markets.looksrare.base_url + '/collections/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
                        target='_blank'
                        circular
                    />}
                  />
                  <Popup
                    inverted
                    on='hover'
                    position='top center'
                    size='small'
                    content='Etherscan'
                    trigger={<Image
                        src='./etherscan.webp'
                        as='a'
                        size='small'
                        href={this.state.markets.markets.etherscan.base_url + '/nft/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
                        target='_blank'
                        circular
                    />}
                  />
                  </div>
                  </Card.Content>
                  <_Card payload={domain} key={domain.name} rates={this.state.rates} rr={this.state.reverse_records.reverse_records[domain.owner]}/>
                </Card>
              )
            ))}

            {this.state.expiringin_payload == null ? (<div></div>) : 
            (
              this.state.expiringin_payload.domains.map(domain => (
                <Card centered fluid>
                  <Card.Content extra>
                  <div className='ui four buttons' id='card_header'>
                    <Popup
                      inverted
                      on='hover'
                      position='top center'
                      size='small'
                      content='Opensea'
                      trigger={<Image
                          src='./opensea.png'
                          as='a'
                          size='small'
                          href={this.state.markets.markets.opensea.base_url + '/assets/ethereum/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
                          target='_blank'
                          circular
                      />}
                    />
                    <Popup
                      inverted
                      on='hover'
                      position='top center'
                      size='small'
                      content='ENS Vision'
                      trigger={<Image
                          src='./ensvision.jpg'
                          as='a'
                          size='small'
                          href={this.state.markets.markets.ensvision.base_url + '/name/' + domain.name}
                          target='_blank'
                          circular
                      />}
                    />
                    <Popup
                      inverted
                      on='hover'
                      position='top center'
                      size='small'
                      content='LooksRare'
                      trigger={<Image
                          src='./looksrare.jpg'
                          as='a'
                          size='small'
                          href={this.state.markets.markets.looksrare.base_url + '/collections/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
                          target='_blank'
                          circular
                      />}
                    />
                    <Popup
                      inverted
                      on='hover'
                      position='top center'
                      size='small'
                      content='Etherscan'
                      trigger={<Image
                          src='./etherscan.webp'
                          as='a'
                          size='small'
                          href={this.state.markets.markets.etherscan.base_url + '/nft/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
                          target='_blank'
                          circular
                      />}
                    />
                  </div>
                  </Card.Content>
                  <_Card payload={domain} key={domain.name} rates={this.state.rates} rr={this.state.reverse_records.reverse_records[domain.owner]}/>
                </Card>
              )
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