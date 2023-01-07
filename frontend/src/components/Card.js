import React from 'react'
import { useEffect, useState } from "react";
import axios from 'axios';
import { Card, Image, Progress } from 'semantic-ui-react'
import {
    handlePremium,
    handleRatio,
    handleStatus,
    handleColor,
    handleFooter,
    handleName,
    handleReverseRecord}
from "../utils.js"



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

// const HandleRR = (payload) => {
//     const [rr, setRR] = useState([]);
//     const [own, setOwn] = useState([]);

//     useEffect(() => {
//         async function middleware() {
//             try {
//                 await console.log(`Records: ${JSON.stringify(payload.rr.reverse_records)}`)
//                 await setOwn(payload.payload.owner);
//                 await setRR(payload.rr.reverse_records[own]);
//             } catch (err) {
//                 console.log(err);
//             }
//         }
//         middleware();
//     }, []);

//     console.log(`Own: ${JSON.stringify(own)}`)
//     console.log(`RR: ${JSON.stringify(rr)}`)
//     return handleReverseRecord(rr)
// }

function _Card(payload) {
    // console.log(`Records: ${JSON.stringify(payload.rr.reverse_records)}`)
    // console.log(`Owner: ${JSON.stringify(payload.payload.owner)}`)
    // console.log(`Reverse Record: ${JSON.stringify(payload.rr.reverse_records[payload.payload.owner])}`)

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
                <Card.Header textAlign='center'>{handleReverseRecord(payload)}</Card.Header>
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
    // HandleCardContext,
  }
