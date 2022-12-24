// const ethers = require('ethers')
// const fs = require('fs');

import { ethers } from 'ethers';
import fs from 'fs';

import { normalize, hash } from './ens_utils.js';

const BigNumber = ethers.BigNumber
const utils = ethers.utils

try {  
    var data = fs.readFileSync('watchlists/watch_clean.txt').toString().split("\n");
} catch(e) {
    console.log('Error:', e.stack);
}

// try {  
//   var data = [
    // 'RaFFY🚴‍♂️.eTh',
    // '-dragón.eth',
    // 'ニョロゾ.eth',
    // 'faceboоk.eth',
    // '💩💩💩💩',
    // '👨',
    // 'facebook.eth',
    // 'lobo.eth',
    // '٢٧٥',
    // '👑scott',
    // 'lucas🚀.eth',
    // '𓃵𓃵𓃵.eth',
    // '⌐◨‐◨.eth',
    // '1⃣2⃣.eth',
//   ]
// } catch(e) {
//   console.log('Error:', e.stack);
// }

// hash('👨️')
data.forEach(hash);

// normalize('👨')
// data.forEach(normalize);

// data.forEach(unicode_checker)
