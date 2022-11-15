import json
import copy
from typing import Dict
from datetime import datetime, timezone
# from web3 import Web3
from backend.utils.utils import (
    BASIC_TRANSACTION,
    SIGN_SEND_WAIT,
    Web3,
    app
)
from ethereum._base import Web3_Base#, app
from web3.exceptions import TimeExhausted, ContractLogicError
from web3.contract import ConciseContract

# import pdb; pdb.set_trace()


def ens_claw(payload: Dict['str', dict] = None) -> Dict['str', dict]:
    '''
    Gathers owner, expiration, & availability data 
    on domains.
    '''
    w3_obj = Web3_Base()
    payload_copy = copy.deepcopy(payload)
    fails = []

    ## Load abi from https://etherscan.io/address/0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85#code
    abiFile = json.load(open('./ethereum/ENS_Base_Registrar.json'))
    abi = abiFile['abi']

    contract_instance = w3_obj.w3.eth.contract(
        abi=abi,
        address=app.config["ENS_BASE_REGISTRAR_MAINNET"],
    )

    # import pdb; pdb.set_trace()
    # Change files to ETH_Reg....json
    # # Returns premium cost only, ensure domain is in auction when called.
    # fee = contract_instance.functions.rentPrice('alce', 1).call()
    # eth_fee = w3_obj.w3.fromWei(fee, 'ether')

    app.logger.info(f"Gathering metadata on {len(payload_copy.keys())} domains...")
    # Iterate through all domains.
    for domain in payload_copy.keys():
        try:
            payload[domain]['name'] = str(domain)
            avail = contract_instance.functions.\
                    available(int(payload[domain]['hash'])).call()
            payload[domain]['available'] = bool(avail)
        except(Exception) as e:
            app.logger.error(f'available on {domain} - Hash {payload[domain]["hash"]}')

        try: # Get domain expiration.
            expires = contract_instance.functions.\
                        nameExpires(int(payload[domain]['hash'])).call()
        except(Exception) as e:
            app.logger.error(f'NameExpires_Error on {domain} - Hash {payload[domain]["hash"]}')
            payload[domain]['expiration'] = 'null'
            fails.append(domain)
        else: # From int timestamp to datetime.datetime object.
            # Converts expire TS into str DT -> 2122-01-14 01:12:19+00:00
            payload[domain]['expiration'] = datetime.fromtimestamp(expires) if expires != 0 else 'null'

        try: # Get domain owner.
            owner = contract_instance.functions.\
                    ownerOf(int(payload[domain]['hash'])).call()
        except(ContractLogicError) as e: # require(expiries[tokenId] > block.timestamp); IE In Grace or Expired
            payload[domain]['owner'] = 'THROW'
            app.logger.error(f'OwnerOf_Error on {domain} - ' \
                             f'Hash {payload[domain]["hash"]} - ')
            fails.append(domain)
        else:
            payload[domain]['owner'] = str(owner)
    
    app.logger.info(f"Domain metadata aquired...")
    app.logger.info(f'Fail Total {len(fails)} - Fail Queue {fails}')

    return payload

ens_claw({})