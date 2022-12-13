import React from 'react'
import { useEffect, useState } from "react";
import axios from 'axios';
import { Button, Card, Image, Progress, Popup, Label } from 'semantic-ui-react'
import {
    handleRatio,
    handleStatus,
    handleColor,
    handleFooter,
    handleName}
from "../utils.js"

function handleCardHeader(markets, domain) {
    // console.log(`I AM HERE B: ${JSON.stringify(markets)}`)
    // console.log(`domain: ${JSON.stringify(domain)}`)
    return <div>
    <Card.Content extra>
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
            href={markets.opensea.base_url + '/assets/ethereum/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
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
            href={markets.ensvision.base_url + '/name/' + domain.name}
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
            href={markets.looksrare.base_url + '/collections/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
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
          href={markets.etherscan.base_url + '/nft/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/' + domain.hash}
          target='_blank'
          circular
      />}
    />
    </Card.Content>
    </div>
}

const HandleCardContext = (payload) => {
    const [premium, setPremium] = useState([]);
    const [rates, setRates] = useState([]);

    useEffect(() => {
        async function fetchData() {
            try {
                if (payload.payload.status === 'IN_AUCTION') {
                    const res = await axios.get(`http://127.0.0.1:5000/api/v1/getPremium?domain=${payload.payload.name}&duration=1`);
                    setPremium(res.data);

                    const rates = await axios.get(`https://api.coinbase.com/v2/exchange-rates?currency=ETH`);
                    console.log(`rates: ${JSON.stringify(rates)}`)
                    // console.log(`rates: ${JSON.stringify(rates.data.data.rates.USD)}`)
                    setRates(rates.data.data.rates.USD);
                }
            } catch (err) {
                console.log(err);
            }
        }
        fetchData();
    }, []);

    if (payload.payload.status === 'IN_AUCTION') {
        if (premium.premium_in_eth != null) {
            let eth_price = premium.premium_in_eth.slice(0, 6)
            let usd_price = (rates * premium.premium_in_eth).toFixed(2)
            return <div style={{ 'color': 'green' }}>
                Premium: {(premium.premium_in_eth == null ? (null) : (`${eth_price}ETH | ${usd_price.toLocaleString()}USD`))}
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



function _Card(payload) {
    // console.log(`I AM HERE PAYLOAD: ${JSON.stringify(payload)}`)
    return (
        <div>
        <Card style={{height:'450px'}}>
            {/* {console.log(`Deck payload 1: ${JSON.stringify(payload.payload)}`)} */}
            <Card.Content >
                <Image
                    // centered
                    src='./hawk.png'
                    size='medium'
                />
                <Card.Header textAlign='center'>{handleName(payload)}</Card.Header>
                <Card.Meta>{HandleCardContext(payload)}</Card.Meta>
                <Card.Description>
                    {handleStatus(payload)}
                </Card.Description>
            </Card.Content>

            <Card.Content style={{ 'backgroundColor': handleColor(payload) }}>
                <Progress percent={handleRatio(payload)} progress>{handleFooter(payload, "card")}</Progress>
            </Card.Content>
        </Card>
        </div>
    )
}

// export default _Card
export {
    _Card,
    HandleCardContext,
  }