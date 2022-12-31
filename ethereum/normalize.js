import fs from 'fs';
import { normalize, hash } from './ens_utils.js';
/**
 * Ensures words are namepreped & ens compatible
*/

let data = []
try {
    // If terminal argv are present, use those values.
    // Needed so I can use subprocess to run node code in
    // python code.
     // ex. node ethereum/normalize.js lobo toro --> [ 'lobo', 'toro' ]
    data = process.argv.slice(2);

    if (data.length == 0) {
        data = fs.readFileSync('watchlists/watch_clean.txt').toString().split("\n");
    }
    // console.log(data);
} catch(e) {
    console.log('Error:', e.stack);
}

// hash('countdooku')
data.forEach(hash);

// console.log(normalize('$Lobo'))
// data.forEach(normalize);
