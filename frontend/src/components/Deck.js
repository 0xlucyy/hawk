import React from 'react'
import { Button, Card, Image } from 'semantic-ui-react'


function Deck(payload) {
    return (
    <div id="deck">
    <Card>
        {/* {console.log(`Deck payload: ${JSON.stringify(payload.payload)}`)} */}
        <Card.Content>
            <Image
                floated='right'
                size='mini'
                // src='../../public/favicon.ico'
                // src='./logo512.png'
                // src='./public/logo512.png'
            />
            <Card.Header>{payload.payload.name}</Card.Header>
            <Card.Meta>Meta</Card.Meta>
            <Card.Description>
            Steve wants to add you {payload.payload.name} to the group <strong>best friends</strong>
            </Card.Description>
        </Card.Content>
        <Card.Content extra>
            <div className='ui two buttons'>
            <Button basic color='green'>
                Approve
            </Button>
            <Button basic color='red'>
                Decline
            </Button>
            </div>
        </Card.Content>
    </Card>
    </div>
    )
  }

  export default Deck
