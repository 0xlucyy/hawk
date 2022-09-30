const ethers = require('ethers')
const fs = require('fs');

const BigNumber = ethers.BigNumber
const utils = ethers.utils

try {  
    var data = fs.readFileSync('ethereum/watch_list.txt').toString().split("\n");
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

// hash('test')
data.forEach(hash);