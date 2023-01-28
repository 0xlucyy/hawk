import { Button, Label, Popup } from 'semantic-ui-react'
import React from 'react';

import Onboard from '@web3-onboard/core'
import injectedModule from '@web3-onboard/injected-wallets'
import { ethers } from 'ethers';
import { SiweMessage } from 'siwe';


const domain = window.location.host;
const origin = window.location.origin;

const injected = injectedModule()
const wallets = [injected]

const chains = [
  {
    id: 1,
    token: 'ETH',
    label: 'Ethereum Mainnet',
    rpcUrl: 'http://geth.dappnode:8545'
  },
  {
    id: 137,
    token: 'MATIC',
    label: 'Matic Mainnet',
    rpcUrl: 'https://matic-mainnet.chainstacklabs.com'
  }
]

const appMetadata = {
  name: 'ENS Hawk',
  icon: './hawk.png',
  logo: './hawk.png',
  description: 'TESTING THE DESCRIPTION',
  recommendedInjectedWallets: [
    { name: 'Coinbase', url: 'https://wallet.coinbase.com/' },
    { name: 'MetaMask', url: 'https://metamask.io' }
  ]
}

const onboard = Onboard({
  wallets,
  chains,
  appMetadata
})


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






async function createSiweMessage(address, domain) {
  /**
   * Create an EIP-4361 message for a web3 wallet to sign.
   * https://eips.ethereum.org/EIPS/eip-4361
   */
  const req = await fetch("http://127.0.0.1:5000/api/v1/nonce", {
    method : 'GET',
    headers: {
      "Accept" : "application/json",
      "Content-Type" : "application/json"
    }
  });
  const data = await req.json();
  const _nonce = data.data

  const message = new SiweMessage({
    domain: domain,
    address: address,
    statement: 'SIWE to ENSHawk.',
    uri: domain,
    version: '1',
    chainId: '1',
    nonce: _nonce,
    resources: ['https://enshawk.eth'],
  });

  return message.prepareMessage();
}


async function connectWeb3Wallet() {
  /**
   * Try to connect a web3 wallet. If successful,
   * get a provider.
   */
  const connectedWallet = await onboard.connectWallet()

    // Create Provider.
  if (connectedWallet[0]) {
    const ethersProvider = await new ethers.providers.Web3Provider(
      connectedWallet[0].provider,
      'any'
    )
    return [ethersProvider, connectedWallet]
  } else {
    return [false, false]
  }
}


async function signVerifyMessage(connectedWallet, ethersProvider) {
  /**
   * 
   */
  if (connectedWallet[0] != false) {

    // Create a Signer.
    const signer = await ethersProvider.getSigner()
    
    // Create SIWE message.
    const siweMessage = await createSiweMessage(connectedWallet[0].accounts[0].address, domain)

    // Sign message.
    const signature = await signer.signMessage(siweMessage)

    // Verify signature.
    let verified_address = await ethers.utils.verifyMessage(siweMessage, signature);
    
    const address = await signer.getAddress();
    if (verified_address != address) {
      console.log("verified: FALSE");
      return false
    }
    else {
      console.log("verified: ", verified_address);
      return verified_address
    }
  }

  // const res = await fetch(`${BACKEND_ADDR}/verify`, {
  //     method: "POST",
  //     headers: {
  //         'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify({ message, signature }),
  //     credentials: 'include'
  // });
  console.log('THIS IS WORKING');
}

// async function getInformation() {
//   const res = await fetch(`${BACKEND_ADDR}/personal_information`, {
//       credentials: 'include',
//   });
//   console.log(await res.text());
// }


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
  createSiweMessage,
  connectWeb3Wallet,
  signVerifyMessage
}