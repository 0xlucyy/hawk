import React from 'react'
import { Button, Card, Image, Progress, Popup } from 'semantic-ui-react'

// Expiration -> 90 days of grace -> 21 days of auction -> free_pool
function ratio(payload) {
    const today = new Date();
    const start = new Date(payload.payload.expiration);
    const end = new Date(payload.payload.auction);
    const p = Math.round(((today - start) / (end - start)) * 100);

    // console.log(`start: ${start}`)
    // console.log(`end: ${end}`)
    // console.log(`today: ${today}`)
    // console.log(`p: ${p}`)

    return p;
}

function color(payload) {
    const free_to_register = 'green'
    const in_grace = 'yellow'
    const in_auction = 'red'

    const p = ratio(payload)

    if (p >= 100) {
        return free_to_register
    }
    else if (p < 100 && p > 0) {
        return in_auction
    }
    else if (p >= 0) {
        return in_grace
    }
}

function Deck(payload) {
    return (
    // <div id="deck">
    <Card centered color={color(payload)} style={{width: '250px', height: '520px'}}>
        <Card.Content extra>
            <div className='ui three buttons' id='card_header'>
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
            />
            </div>
        </Card.Content>
        {/* {console.log(`Deck payload: ${JSON.stringify(payload.payload)}`)} */}
        <Card.Content>
            <Image
                // centered
                src='./hawk.png'
            />
            <Card.Header textAlign='center'>{payload.payload.name}</Card.Header>
            <Card.Meta>Expiration: {payload.payload.expiration}</Card.Meta>
            <Card.Description>
            Status: {payload.payload.grace}
            </Card.Description>
        </Card.Content>

        <Card.Content>
        <Progress percent={ratio(payload)} progress>Auction ends {payload.payload.auction}</Progress>
        </Card.Content>
        {/* <Progress percent={ratio(payload)} progress>Auction ends {payload.payload.auction}</Progress> */}
        
    </Card>
    // {/* </div> */}
    )
  }

  export default Deck
