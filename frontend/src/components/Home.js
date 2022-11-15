import React, { Component } from 'react'
import { Input, Menu, Button, Card, Container, Image, Popup } from 'semantic-ui-react'
import Deck from './Deck.js'

export default class Home extends Component {
    state = {
        payload: null,
        markets: null,
        loading: false,
        timeout: 30,
        days: 0,
    
        // Error related.
        error: false,
        errorMessage: '',
        hidden: true,
      };
    
      loadData = async (e, value) => {
        e.preventDefault();
        console.log(`Loading domain & market data....`)

        let response = await fetch(`http://127.0.0.1:5000/api/v1/allMarkets?order=asc`);
        const markets = await response.json();
        // console.log(`000 markets: ${JSON.stringify(markets)}`)
        await this.setState({ markets });

        response = await fetch(`http://127.0.0.1:5000/api/v1/expiredDomains`);
        const payload = await response.json();
        await this.setState({ payload });
        // return payload;
      };
    
      handleDismiss = async (e, value) => {
        e.preventDefault();
        console.log(`handleDismiss`);
        await this.setState({ 
          hidden: false,
          error: true,
          errorMessage: ''
        });
        // console.log(`Days: ${this.state.days}`);
        // console.log(`payload: ${JSON.stringify(this.state.payload)}`);
      };
    

  render() {
    return (
    <div className="Home" id="home">
    <h2 style = {{color: "green"}}> ENS Hawk </h2>

    <Input 
    placeholder="Days"
    onChange={ (event) => {
        this.setState({ days: event.target.value });
    }}
    >
    </Input>
    <Button onClick={this.loadData}
            className="icon"
            labelPosition='left'>
            loadData!
    </Button>
    < div style = {{marginTop: 100}}>
    <Container>
        <div>
        <Card.Group itemsPerRow="5" textAlign="center" className='domains'>
            {this.state.payload == null ? (<div>Load data...</div>) : 
            (
                this.state.payload.domains.map(domain => (
                  <Card centered style={{width: '250px', height: '520px'}}>
                    <Card.Content extra>
                    <div className='ui three buttons' id='card_header'>
                    {console.log(`MARKETS: ${JSON.stringify(this.state.markets)}`)}
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
                            href='https://google.com'
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
                            href='https://google.com'
                            target='_blank'
                            circular
                        />}
                    />{`TESTING: ${this.state.markets}`}
                    </div>
                    </Card.Content>
                    <Deck payload={domain} key={domain.name}/>
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