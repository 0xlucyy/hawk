import React, { Component } from 'react'
import { Input, Menu, Button, Card, Container, Image, Popup, Progress } from 'semantic-ui-react'
import {_Card, HandleCardContext} from './Card.js'
// console.log(`data: ${JSON.stringify(markets)}`)


export default class Expiring extends Component {
  state = {
    payload: null,
    expiringin_payload: null,
    expired_payload: null,
    markets: null,
    loading: false,
    timeout: 30,
    days: null,
    view: 'card',
    premium: null,
    rates: null,

    // Error related.
    error: false,
    errorMessage: '',
    hidden: true,
  };

  load_market_data = async (e, value) => {
    if (this.state.markets === null) {
      console.log(`Loading market data....`)
      let response = await fetch(`http://127.0.0.1:5000/api/v1/allMarkets?order=asc`);
      const markets = await response.json();
      this.setState({ markets });
    }
  }

  // get_premium_data = async (e, value) => {
  //   e.preventDefault();
  //   let premium = {}
  //   let rates = null

  //   try {
  //     if (this.state.payload.status === 'IN_AUCTION') {
  //         console.log(`Getting premium for ${value}`)
  //         let response = await fetch(`http://127.0.0.1:5000/api/v1/getPremium?domain=${value}&duration=1`);
  //         premium = await response.json();
  //         console.log(`premium: ${JSON.stringify(premium)}`)
  //         this.setState({premium});

  //         rates = await fetch(`https://api.coinbase.com/v2/exchange-rates?currency=ETH`);
  //         console.log(`rates: ${JSON.stringify(rates.data.data.rates.USD)}`)
  //         this.setState({rates: rates.data.data.rates.USD});
  //     }
  //   } catch (err) {
  //       console.log(err);
  //   }

  //   if (this.state.payload.status === 'IN_AUCTION') {
  //     // console.log(`rates: ${JSON.stringify(rates.data.rates.USD.slice(0,7))}`)
  //     if (premium.premium_in_eth != null) {
  //         let eth_price = premium.premium_in_eth.slice(0, 6)
  //         let usd_price = (rates * premium.premium_in_eth).toFixed(2)
  //         return <div style={{ 'color': 'green' }}>
  //             Premium: {(premium.premium_in_eth == null ? (null) : (`${eth_price}ETH | ${usd_price.toLocaleString()}USD`))}
  //         </div>
  //     }
  //   } else if (this.state.payload.status === 'IN_GRACE') {
  //       return `Grace Expires: ${this.state.payload.grace}`
  //   } else if (this.state.payload.status === 'BEING_HELD') {
  //       return `Expiration: ${this.state.payload.expiration}`
  //   } else if (this.state.payload.status === 'FREE') {
  //       return `FREE`
  //   }
  //   return `ERROR`
  // }

  expired = async (e, value) => {
    e.preventDefault();
    await this.load_market_data()

    console.log(`Loading expired domain data....`)
    let response = await fetch(`http://127.0.0.1:5000/api/v1/expiredDomains`);
    const expired_payload = await response.json();
    await this.setState({ expiringin_payload: null });
    await this.setState({ expired_payload });
  };

  expiring_in = async (e, value) => {
    e.preventDefault();
    if (this.state.days === null) {
      await this.setState({ days: 10 });
    }
    await this.load_market_data()

    console.log(`Loading expiring domains within ${this.state.days} days....`)
    let response = await fetch(`http://127.0.0.1:5000/api/v1/expiringDomains?days=${this.state.days}`);
    const expiringin_payload = await response.json();
    await this.setState({ expired_payload: null });
    await this.setState({ expiringin_payload });
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


  render() {
    return (
    <div className="Home" id="home">
    <h2 style = {{color: "green"}}> ENS Hawk </h2>

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
            labelPosition='left'>
            Days until expiration
    </Button>
    <Button onClick={this.expired}
            className="icon"
            labelPosition='left'>
            All Expired domains
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
                    {/* {console.log(`MARKETS: ${JSON.stringify(this.state.markets)}`)} */}
                    {/* <div>{HandleCardHeader(this.state.markets.markets, domain)}</div> */}
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
                    <_Card payload={domain} key={domain.name}/>
                  </Card>
                )
              )
            )
            }

            {this.state.expiringin_payload == null ? (<div></div>) : 
            (
                this.state.expiringin_payload.expiring_domains.map(domain => (
                  // <Card centered style={{width: '250px', height: '520px'}}>
                  <Card centered fluid>
                    {/* <Card.Content extra> */}
                    {/* <div className='ui four buttons' id='card_header'> */}
                    {/* {console.log(`MARKETS: ${JSON.stringify(this.state.markets)}`)} */}
                    {/* {handleCardHeader(this.state.markets.markets, domain)} */}
                    <handleCardHeader markets={this.state.markets.markets} domain={domain}/>
                    {/* <Popup
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
                      content='Etherscane'
                      trigger={<Image
                          src='./etherscan.webp'
                          as='a'
                          size='small'
                          href={this.state.markets.markets.etherscan.base_url + '/nft/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
                          target='_blank'
                          circular
                      />}
                    /> */}
                    {/* </div> */}
                    {/* </Card.Content> */}
                    <_Card payload={domain} key={domain.name} />
                    {/* {_Card(domain)} */}
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