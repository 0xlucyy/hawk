import React from 'react'
import { Button, Card, Image, Progress, Popup } from 'semantic-ui-react'

const free_to_register = 'green'
const in_grace = 'yellow'
const in_auction = 'red'

// Expiration -> 90 days of grace -> 21 days of auction -> free_pool
function ratio(payload) {
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

function card_footer(payload) {
    const now = new Date();
    const auction = new Date(payload.payload.auction);
    const grace = new Date(payload.payload.grace);
    const expiration = new Date(payload.payload.expiration);

    if (now > auction) { // domain is free to claim.
        return <Button as='a' target='_blank' href="https://google.com" inverted circular style={{'background-color': 'grey'}}>Claim</Button>
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


function color(payload) {
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

function Deck(payload) {
    return (
    <Card centered style={{width: '250px', height: '520px'}} >
        {/* {console.log(`Deck payload 1: ${JSON.stringify(payload.payload)}`)} */}
        <Card.Content>
            <Image
                // centered
                src='./hawk.png'
                size='medium'
            />
            <Card.Header textAlign='center' as='h1'>{payload.payload.name}.eth</Card.Header>
            <Card.Meta>Expiration: {payload.payload.expiration}</Card.Meta>
            <Card.Description>
            Status: {payload.payload.status}
            </Card.Description>
        </Card.Content>

        <Card.Content style={{'background-color': color(payload)}}>
        <Progress percent={ratio(payload)} progress>{card_footer(payload)}</Progress>
        </Card.Content>

    </Card>
    )
  }

  export default Deck
