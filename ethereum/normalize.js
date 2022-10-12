const ethers = require('ethers')
const fs = require('fs');

const BigNumber = ethers.BigNumber
const utils = ethers.utils

try {  
    var data = fs.readFileSync('watchlists/watch_clean.txt').toString().split("\n");
} catch(e) {
    console.log('Error:', e.stack);
}

function hash(value) {
    try {  
        const labelHash = utils.keccak256(utils.toUtf8Bytes(value))
        const tokenId = BigNumber.from(labelHash).toString()
        console.log(value + "," + tokenId)
    } catch(e) {
        console.log('Error:', e.stack);
    }
}

// hash('tihdiascnisajdn98hfj')
data.forEach(hash);