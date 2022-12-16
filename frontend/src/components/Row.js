import React from 'react'
import { useEffect, useState } from "react";
import axios from 'axios';
import { Table, Button, Progress } from 'semantic-ui-react'
import {
    handleRatio,
    handleStatus,
    handleColor,
    handleFooter,
    handleName,
    handleOwner
}
from "../utils.js"



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
                    console.log(`rates: ${JSON.stringify(rates.data.data.rates.USD)}`)
                    setRates(rates.data.data.rates.USD);
                }
            } catch (err) {
                console.log(err);
            }
        }
        fetchData();
    }, []);

    if (payload.payload.status === 'IN_AUCTION') {
        // console.log(`rates: ${JSON.stringify(rates.data.rates.USD.slice(0,7))}`)
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
        return <div></div>
    }
    return `ERROR`
}

function Row(payload) {
    return (
    <Table.Row >
        <Table.Cell>
            {handleName(payload)}
        </Table.Cell>

        <Table.Cell style = {{'color': handleColor(payload)}}>
            {handleStatus(payload)}
        </Table.Cell>{/* Status column */}

        <Table.Cell style = {{'color': handleColor(payload)}}>
            {HandleCardContext(payload)}
        </Table.Cell>{/* Context column */}

        <Table.Cell textAlign={'middle'} collapsing={true} style = {{'color': handleColor(payload)}}>
            {handleFooter(payload, 'row')}
        </Table.Cell>{/* Info column */}

        <Table.Cell style = {{'color': handleColor(payload)}}>
            {handleOwner(payload, 'row')}
        </Table.Cell>{/* Owner column */}
        
        {/* <Table.Cell></Table.Cell> */}
    </Table.Row>
    )
  }

  export default Row
