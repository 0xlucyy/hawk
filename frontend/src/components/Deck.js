import React from 'react'
import { useEffect, useState } from "react";
import axios from 'axios';
import { Button, Card, Image, Progress, Popup } from 'semantic-ui-react'

const free_to_register = 'green'
const in_grace = 'yellow'
const in_auction = 'red'

// Expiration -> 90 days of grace -> 21 days of auction -> free_pool
function handleRatio(payload) {
    const today = new Date();
    const start = new Date(payload.payload.expiration);
    const end = new Date(payload.payload.auction);
    const p = Math.round(((today - start) / (end - start)) * 100);
    return p;
}

function days_between(date1, date2) {
    // The number of milliseconds in one day
    const _MS_PER_DAY = 1000 * 60 * 60 * 24;
    // Calculate the difference in milliseconds
    const differenceMs = Math.abs(date1 - date2);
    // return Math.round(differenceMs / _MS_PER_DAY);

    const days = Math.round(differenceMs / _MS_PER_DAY)
    const minutes = Math.floor((differenceMs / 1000 / 60) % 60);
    const hours = Math.floor((differenceMs / 1000 / 60 / 60) % 24);

    let day_str = days + " day" + (days > 1 ? "s " : "")
    let hr_str = hours + ' hour' + (hours > 1 ? "s " : "")
    let min_str = minutes + " minute" + (minutes > 1 ? "s " : "")

    const total = (days > 1 ? day_str : "") + (hours > 1 ? hr_str : "") + " & " + (minutes > 1 ? min_str : "")

    return total
}

function handleFooter(payload) {
    const now = new Date();
    const auction = new Date(payload.payload.auction);
    const grace = new Date(payload.payload.grace);
    const expiration = new Date(payload.payload.expiration);

    if (now > auction) { // domain is free to claim.
        let _href = 'https://app.ens.domains/name/' + payload.payload.name + '.eth/register'
        return <Button as='a' target='_blank' href={_href} inverted circular style={{'background-color': 'grey'}}>Claim</Button>
    }
    else if (now < auction & now > grace) {
        const auction = new Date(payload.payload.auction);
        return `Auction expires in ${days_between(auction, now)}`
    }
    else if (now > expiration & now < grace) {
        const grace = new Date(payload.payload.grace);
        return `Grace expires in ${days_between(grace, now)}`
    }
    else {
        const expiration = new Date(payload.payload.expiration);
        return `Expires in ${days_between(expiration, now)}`
    }
}

function handleColor(payload) {
    const now = new Date();
    const auction = new Date(payload.payload.auction);
    const grace = new Date(payload.payload.grace);
    const expiration = new Date(payload.payload.expiration);

    if (now > auction) {
        return free_to_register
    }
    else if (now < auction & now > grace) {
        return in_auction
    }
    else if (now > expiration & now < grace) {
        return in_grace
    }
    // else {
    //     return hodl
    // }
}

function handleStatus(payload) {
    let _href = null
    if (payload.payload.status === 'IN_AUCTION') {
        _href = `https://app.ens.domains/name/${payload.payload.name}.eth/register`;
        let response = fetch(_href);
        console.log(``)


        return <Button as='a' target='_blank' href={_href} circular style={{'background-color': handleColor(payload)}}>Domain in Auction. Claim!</Button>
    } else if (payload.payload.status === 'IN_GRACE') {
        _href = `https://app.ens.domains/search/${payload.payload.name}`
        return <Button as='a' target='_blank' href={_href} circular style={{'background-color': handleColor(payload)}}>Domain in Grace. Details!</Button>
    }  else if (payload.payload.status === 'BEING_HELD') {
        _href = `https://app.ens.domains/search/${payload.payload.name}`
        return <Button as='a' target='_blank' href={_href} circular style={{'background-color': handleColor(payload)}}>Domain in Being Held. Details!</Button>

    }
    return payload.payload.status
}


const Test = (payload) => {
    const [posts, setPosts] = useState([]);
    const [rates, setRates] = useState([]);
    
    useEffect( () => { 
        async function fetchData() {
            try {
                if (payload.payload.status === 'IN_AUCTION') {
                    const res = await axios.get(`http://127.0.0.1:5000/api/v1/getPremium?domain=${payload.payload.name}&duration=1`); 
                    await setPosts(res.data);

                    const rates = await axios.get(`https://api.coinbase.com/v2/exchange-rates?currency=ETH`);
                    console.log(`rates: ${JSON.stringify(rates.data.data.rates.USD)}`)
                    await setRates(rates.data.data.rates.USD);
                }
            } catch (err) {
                console.log(err);
            }
        }
        fetchData();
    }, []);

    if (payload.payload.status === 'IN_AUCTION') {
        // console.log(`rates: ${JSON.stringify(rates.data.rates.USD.slice(0,7))}`)
        if (posts.premium_in_eth != null) {
            let eth_price = posts.premium_in_eth.slice(0,6)
            let usd_price = (rates * posts.premium_in_eth).toFixed(2)
            return <div style={{'color': 'green'}}>
            Premium: {(posts.premium_in_eth == null ? (null) : (`${eth_price}ETH | ${usd_price.toLocaleString()}USD`))}
            </div>
        }
    }
    return `Expiration: ${payload.payload.expiration}`
}


function Deck(payload) {
    return (
    <Card centered style={{width: '500px', height: '1000px'}} >
        {/* {console.log(`Deck payload 1: ${JSON.stringify(payload.payload)}`)} */}
        <Card.Content >
            <Image
                // centered
                src='./hawk.png'
                size='medium'
            />
            <Card.Header textAlign='center' as='h1'>{payload.payload.name}.eth</Card.Header>
            <Card.Meta>{Test(payload)}</Card.Meta>
            <Card.Description>
                {handleStatus(payload)}
            </Card.Description>
        </Card.Content>

        <Card.Content style={{'background-color': handleColor(payload)}}>
        <Progress percent={handleRatio(payload)} progress>{handleFooter(payload)}</Progress>
        </Card.Content>
    </Card>
    )
  }

  export default Deck

//   0x770c13284eB073F07d7c88fb787c319d533F785A
