import React, { Component } from 'react'
import { Input, Menu, Button, Card, Container, Image, Popup, Progress } from 'semantic-ui-react'
import {_Card, HandleCardContext, handleCardHeader} from './Card.js'
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

  load_market_data = async () => {
    if (this.state.markets === null) {
      console.log(`Loading market data....`)
      let response = await fetch(`http://127.0.0.1:5000/api/v1/allMarkets?order=asc`);
      const markets = await response.json();
      this.setState({ markets });
    }
  }

  load_rates_data = async () => {
    if (this.state.rates == null) {
      console.log(`Loading rates data from coinbase....`)
      let response = await fetch(`https://api.coinbase.com/v2/exchange-rates?currency=ETH`);
      const rates = await response.json();
      this.setState({ rates });
      // console.log(`Loaded Rates Data: ${JSON.stringify(rates)}`)
    }
  }

  expired = async (e, value) => {
    e.preventDefault();
    await this.load_market_data()
    await this.load_rates_data()

    console.log(`Loading expired domain data....`)
    let response = await fetch(`http://127.0.0.1:5000/api/v1/expiredDomains`);
    const expired_payload = await response.json();
    this.setState({ expiringin_payload: null });
    this.setState({ expired_payload });
  };

  expiring_in = async (e, value) => {
    e.preventDefault();
    if (this.state.days === null) {
      this.setState({ days: 10 });
    }
    await this.load_market_data()
    await this.load_rates_data()

    console.log(`Loading expiring domains within ${this.state.days} days....`)
    let response = await fetch(`http://127.0.0.1:5000/api/v1/expiringDomains?days=${this.state.days}`);
    const expiringin_payload = await response.json();

    this.setState({ expired_payload: null });
    this.setState({ expiringin_payload });
  };

  handleDismiss = async (e, value) => {
    e.preventDefault();
    console.log(`handleDismiss`);
    this.setState({
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
                    <_Card payload={domain} key={domain.name} rates={this.state.rates}/>
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
                    <Card.Content extra>
                    <div className='ui four buttons' id='card_header'>
                    {/* {console.log(`MARKETS: ${JSON.stringify(this.state.markets)}`)} */}
                    {/* {handleCardHeader(this.state.markets.markets, domain)} */}
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
                      content='Etherscane'
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
                    <_Card payload={domain} key={domain.name} rates={this.state.rates}/>
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