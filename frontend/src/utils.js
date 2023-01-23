import { Button, Label, Popup } from 'semantic-ui-react'
import React from 'react';

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

function days_between(date1, date2, view) {
  // The number of milliseconds in one day
  const _MS_PER_DAY = 1000 * 60 * 60 * 24;
  // Calculate the difference in milliseconds
  const differenceMs = Math.abs(date1 - date2);
  // return Math.round(differenceMs / _MS_PER_DAY);

  const days = Math.round(differenceMs / _MS_PER_DAY)
  const minutes = Math.floor((differenceMs / 1000 / 60) % 60);
  const hours = Math.floor((differenceMs / 1000 / 60 / 60) % 24);

  let data = null
  if(view === "row"){
    let day_str = days + "D:"
    let hr_str = hours + 'H:'
    let min_str = minutes + "M"
    data = (days > 1 ? day_str : "") + (hours > 1 ? hr_str : "") + (minutes > 1 ? min_str : "")
  } else if(view === "card") {
    let day_str = days + " day" + (days > 1 ? "s " : "")
    let hr_str = hours + ' hr' + (hours > 1 ? "s " : "")
    let min_str = minutes + " min" + (minutes > 1 ? "s " : "")
    // TODO BUG HERE WHEN ONLY MINUTES ARE LEFT
    // Example: Grace expires in & 57 mins
    data = (days > 1 ? day_str : "") + (hours > 1 ? hr_str : "") + (minutes > 1 ? ` &  ${min_str}` : "")
  }
  return data
}

function handleStatus(payload) {
  let _href = null
  // console.log(`payload is: ${payload}`)

  try {
    // Needed for BulkSearch postSearch page.
    if (payload.payload === undefined) {
      payload.payload = payload
    }
  } catch(e) {
    console.log('[ACTION] Correcting payload ...')
  }
  if (payload.payload.status === 'IN_AUCTION') {
      _href = `https://app.ens.domains/name/${payload.payload.name}.eth/register`;
      // let response = fetch(_href);
      return <Popup position="bottom center" inverted on='hover' size="small" content='ens.domains' trigger={<Button as='a' target='_blank' href={_href} circular style={{'background-color': handleColor(payload)}}>In Auction!</Button>} />
  } else if (payload.payload.status === 'IN_GRACE') {
      _href = `https://app.ens.domains/search/${payload.payload.name}`
      return <Popup position="bottom center" inverted on='hover' size="small" content='ens.domains' trigger={<Button as='a' target='_blank' href={_href} circular style={{'background-color': handleColor(payload)}}>In Grace!</Button>} />
  }  else if (payload.payload.status === 'BEING_HELD') {
      _href = `https://app.ens.domains/search/${payload.payload.name}`
      return <Popup position="bottom center" inverted on='hover' size="small" content='ens.domains' trigger={<Button as='a' target='_blank' href={_href} circular style={{'background-color': handleColor(payload)}}>Being Held!</Button>} />
  }
  _href = `https://app.ens.domains/name/${payload.payload.name}.eth/register`;
  return <Popup position="bottom center" inverted on='hover' size="small"  content='ens.domains' trigger={<Button as='a' target='_blank' href={_href} circular style={{'background-color': handleColor(payload)}}>Claim!</Button>} />
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
}

function handleFooter(payload, view) {
  const now = new Date();
  const auction = new Date(payload.payload.auction);
  const grace = new Date(payload.payload.grace);
  const expiration = new Date(payload.payload.expiration);

  if (now > auction) { // domain is free to claim.
      // let _href = 'https://app.ens.domains/name/' + payload.payload.name + '.eth/register'
      // return <Button as='a' target='_blank' href={_href} inverted circular style={{'background-color': 'grey'}}>Claim</Button>
      return <div>Free</div>
  }
  else if (now < auction & now > grace) {
      const auction = new Date(payload.payload.auction);
      return `Auction expires in ${days_between(auction, now, view)}`
  }
  else if (now > expiration & now < grace) {
      const grace = new Date(payload.payload.grace);
      return `Grace expires in ${days_between(grace, now, view)}`
  }
  else {
      const expiration = new Date(payload.payload.expiration);
      return `Expires in ${days_between(expiration, now, view)}`
  }
}

function handleName(payload) {
  // let _href = `https://app.ens.domains/name/${payload.payload.name}.eth/register`;
  // return <Label size='big' style={{'color': 'orange', 'backgroundColor':'transparent'}} as='a' target='_blank' href={_href}>{payload.payload.name}.eth</Label>
  return <Label size='big' style={{'color': 'orange', 'backgroundColor':'transparent'}}>{payload.payload.name}.eth</Label>
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// This function is only employed in Row.js
function handleOwner(payload) {
  // {(payload.payload.owner == 'THROW' ? 'no_owner' : (payload.payload.owner).substr(0, 13))}
  if (payload.payload.owner === '0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85') {
    return <div>Can be minted!</div>
  } else {
    let _href = 'https://etherscan.io/address/' + payload.payload.owner
    return <div as='a' target='_blank' href={_href}>{(payload.payload.owner).substr(0, 13)}</div>
  }
  // console.log(`Owner: ${payload.payload.owner}`)
  // console.log(`Owner Substr: ${(payload.payload.owner).substr(0, 13)}`)
}

function handlePremium(payload, premium) {
  if (payload.payload.status === 'IN_AUCTION') {
    if (premium.premium_in_eth != null) {
        let eth_premium = ((premium.cost_per_year * premium.years) / payload.rates.data.rates.USD) + parseFloat(premium.premium_in_eth)
        let usd_premium = ((payload.rates.data.rates.USD * premium.premium_in_eth) + (premium.cost_per_year * premium.years))
        return <div style={{ 'color': 'green' }}>
            Premium: {(premium.premium_in_eth == null ? (null) : (`${eth_premium.toFixed(4)}ETH | ${usd_premium.toFixed(2)}USD`))}
        </div>
    }
  } else if (payload.payload.status === 'IN_GRACE') {
      return `Grace Expires: ${payload.payload.grace}`
  } else if (payload.payload.status === 'BEING_HELD') {
      return `Expiration: ${payload.payload.expiration}`
  } else if (payload.payload.status === 'FREE') {
      return `FREE`
  }
  return `ERROR`
}


function handleReverseRecord(payload) {
  let owner = payload.payload.owner;
  try {
    // debugger;
    owner = payload.rr.reverse_records[payload.payload.owner]
  } catch (e) {}
  return <Label size='medium' style={{'color': 'black', 'backgroundColor':'transparent'}}>Owner: {(owner == null ? (payload.payload.owner).substr(0, 15) : (owner).substr(0, 15))}{(owner == null ? <div></div> : ".eth")}</Label>
}


export {
  handleRatio,
  handleStatus,
  handleColor,
  handleFooter,
  handleName,
  handleOwner,
  handlePremium,
  capitalizeFirstLetter,
  handleReverseRecord,
}