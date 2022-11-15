import React from 'react'
import { Table, Button, Progress } from 'semantic-ui-react'

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

    let day_str = days + "D:"
    let hr_str = hours + 'H:'
    let min_str = minutes + "M"

    const total = (days > 1 ? day_str : "") + (hours > 1 ? hr_str : "") + (minutes > 1 ? min_str : "")

    return total
}

function row_footer(payload) {
    const now = new Date();
    const auction = new Date(payload.payload.auction);
    const grace = new Date(payload.payload.grace);
    const expiration = new Date(payload.payload.expiration);

    if (now > auction) { // domain is free to claim.
        return <Button as='a' target='_blank' href="https://google.com" inverted circular style={{'background-color': 'grey'}}>Claim</Button>
    }
    else if (now < auction & now > grace) {
        const auction = new Date(payload.payload.auction);
        return `Auction end: ${days_between(auction, now)}`
    }
    else if (now > expiration & now < grace) {
        const grace = new Date(payload.payload.grace);
        return `Grace ends: ${days_between(grace, now)}`
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
}

function Row(payload) {
    return (
    <Table.Row >
        <Table.Cell style = {{'color': color(payload)}}>{payload.payload.name}</Table.Cell>
        <Table.Cell style = {{'color': color(payload)}}>{payload.payload.status}</Table.Cell>
        <Table.Cell style = {{'color': color(payload)}}>{(payload.payload.expiration == null ? 'Free to register' : payload.payload.expiration)}</Table.Cell>
        <Table.Cell style = {{'color': color(payload)}}>{(payload.payload.grace == null ? 'Free to register' : payload.payload.grace)}</Table.Cell>
        <Table.Cell style = {{'color': color(payload)}}>{(payload.payload.auction == null ? 'Free to register' : payload.payload.auction)}</Table.Cell>
        <Table.Cell style = {{'color': color(payload)}}>{(payload.payload.owner == 'FREE' ? 'no_owner' : (payload.payload.owner).substr(0, 13))}</Table.Cell>
        <Table.Cell style = {{'color': color(payload)}}>{row_footer(payload)}</Table.Cell>
        <Table.Cell></Table.Cell>
    </Table.Row>
    )
  }

  export default Row
