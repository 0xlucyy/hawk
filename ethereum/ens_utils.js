import { ens_normalize } from '@adraffy/ens-normalize';
import { ethers } from 'ethers';


function normalize(name) {
  try {
    const normalized = ens_normalize(name);
    // console.log(`Name: ${ens_beautify(normalized)} - PASS`)
    return normalized
  } catch(e) {
    // console.log(`Error: ${e.stack} - Name: ${name} - FAIL...`);
    return false
  }
}

function hash(name) {
  const BigNumber = ethers.BigNumber
  const utils = ethers.utils

  try {
    let normalized = normalize(name)
    if (normalized !== false) {
      const labelHash = utils.keccak256(utils.toUtf8Bytes(normalized))
      const tokenId = BigNumber.from(labelHash).toString()
      console.log(normalized + "," + tokenId)
    }
  } catch(e) {
    console.log('Error:', e.stack, "Name: ", name);
  }
}


export {
  hash,
  normalize,
}
