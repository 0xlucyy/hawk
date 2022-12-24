import React from 'react'
import { useEffect, useState } from "react";
import axios from 'axios';
import { Button, Card, Image, Progress, Popup, Label } from 'semantic-ui-react'
import {
    handlePremium,
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

    useEffect(() => {
        async function fetchData() {
            try {
                if (payload.payload.status === 'IN_AUCTION') {
                    const res = await axios.get(`http://127.0.0.1:5000/api/v1/getPremium?domain=${payload.payload.name}&duration=1`);
                    setPremium(res.data);
                }
            } catch (err) {
                console.log(err);
            }
        }
        fetchData();
    }, []);

    return handlePremium(payload, premium)
}



function _Card(payload) {
    // console.log(`I AM HERE PAYLOAD: ${JSON.stringify(payload)}`)
    // console.log(`2: ${JSON.stringify(payload.rates)}`)
    // console.log(`2: ${JSON.stringify(payload.rates.data.rates.USD)}`)

    return (
        <div>
        <Card style={{height:'440px'}}>
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
    handleCardHeader
  }


// TODO DappNode REMOTE
// [Interface]
// PrivateKey = kIncvnBH8XGDv3UX9zyV7fcpfxqrvZblwpkAjDQ1O2k=
// ListenPort = 51820
// Address = 10.24.0.5/32
// DNS = 172.33.1.2, 10.20.0.2

// [Peer]
// PublicKey = tbwLVl0wS46u0JNsfDZDPo7K3KSRY+gyvmvqDPrItgQ=
// AllowedIPs = 172.33.0.0/16, 10.20.0.0/24
// Endpoint = 65ebd1c1e30d76c0.dyndns.dappnode.io:51820
