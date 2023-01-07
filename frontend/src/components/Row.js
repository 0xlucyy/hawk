import React from 'react'
import { useEffect, useState } from "react";
import axios from 'axios';
import { Table } from 'semantic-ui-react'
import {
    // handleRatio,
    handleStatus,
    handleColor,
    handleFooter,
    handleName,
    handleOwner,
    handlePremium,
}
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
