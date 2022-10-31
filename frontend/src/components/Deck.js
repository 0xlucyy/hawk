import React from 'react'
import { Button, Card, Image, Progress } from 'semantic-ui-react'


function Deck(payload) {
    return (
    // <div id="deck">
    <Card>
        {/* {console.log(`Deck payload: ${JSON.stringify(payload.payload)}`)} */}
        <Card.Content>
            <Image
                centered
                src='./hawk.png'
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
        <Progress percent={11} />
    </Card>
    // {/* </div> */}
    )
  }

  export default Deck
