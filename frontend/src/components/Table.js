import React from 'react'
import { Table, Button } from 'semantic-ui-react'
import _Row from './Row.js';

// // Expiration -> 90 days of grace -> 21 days of auction -> free_pool
// function ratio(payload) {
//     const today = new Date();
//     const start = new Date(payload.payload.expiration);
//     const end = new Date(payload.payload.auction);
//     const p = Math.round(((today - start) / (end - start)) * 100);
//     return p;
// }

// function color(payload) {
//     const free_to_register = 'green'
//     const in_grace = 'yellow'
//     const in_auction = 'red'
//     const p = ratio(payload)

//     if (p >= 100) {
//         return free_to_register
//     }
//     else if (p < 100 && p > 0) {
//         return in_auction
//     }
//     else if (p >= 0) {
//         return in_grace
//     }
// }

export default class _Table extends React.Component {
    state = {
        payload: null,
        loading: false,
        timeout: 30,
        days: 0,
        markets: null,
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
        }
    }

    load_all_domains = async (e, value) => {
        e.preventDefault();
        this.setState({ loading: true });

        // await this.load_market_data()
        await this.load_rates_data()

        const response = await fetch(`http://127.0.0.1:5000/api/v1/allDomains?order=asc`);
        const payload = await response.json();

        this.setState({ payload });
        this.setState({ loading: false });
        // console.log(`payload: ${JSON.stringify(this.state.payload)}`);

        return payload;
    };

    render() {
    return (
    <div id="_table">
    <Button onClick={this.load_all_domains}
            className="icon"
            color="black"
            loading={this.state.loading}>
            {this.state.payload == null ? (<div>Load data</div>) : (<div>Refresh data</div>)}
    </Button>
    <Table singleLine color={'black'} inverted striped>
        <Table.Header>
            <Table.Row>
                <Table.HeaderCell>.eth Name</Table.HeaderCell>
                <Table.HeaderCell>Status</Table.HeaderCell>
                <Table.HeaderCell>Context</Table.HeaderCell>
                {/* <Table.HeaderCell>Grace Expiration</Table.HeaderCell>
                <Table.HeaderCell>Auction Expiration</Table.HeaderCell> */}
                <Table.HeaderCell>Info</Table.HeaderCell>
                <Table.HeaderCell>Owner</Table.HeaderCell>                
            </Table.Row>
        </Table.Header>

        <Table.Body>
        {this.state.payload == null ? (<div></div>) : 
            (
                this.state.payload.domains.map(domain => 
                    // console.log(`WORKING?: ${JSON.stringify(domain)}`)
                    // console.log('1212121')
                    <_Row payload={domain} key={domain.name} rates={this.state.rates}/>
                )
            )
        }
        </Table.Body>
    </Table>
    </div>
    )
  }}
