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

    app.logger.info(f"Gathering metadata on {len(payload_copy.keys())} domains...")
    # Iterate through all domains.
    for domain in payload_copy.keys():
        payload[domain]['name'] = str(domain)
        avail = contract_instance.functions.\
                available(int(payload[domain]['hash'])).call()
        payload[domain]['available'] = bool(avail)

        if bool(avail) == True: # Domain can be minted right now.
            payload[domain]['expiration'] = 'null'
            payload[domain]['owner'] = 'not owned'
        else: # Domain is either expiring, in grace, or being held.
            try: # Get domain expiration.
                expires = contract_instance.functions.\
                          nameExpires(int(payload[domain]['hash'])).call()
            except(Exception) as e:
                app.logger.error(f'NameExpires_Error on {domain} - Hash {payload[domain]["hash"]}')
                fails.append(domain)
            else: # From int timestamp to datetime.datetime object.
                # Converts expire TS into str DT -> 2122-01-14 01:12:19+00:00
                payload[domain]['expiration'] = datetime.fromtimestamp(expires)

            try: # Get domain owner.
                owner = contract_instance.functions.\
                        ownerOf(int(payload[domain]['hash'])).call()
            except(ContractLogicError) as e: # require(expiries[tokenId] > block.timestamp); IE In Grace or Expired
                payload[domain]['owner'] = app.config['ENS_GRACE_AUCTION']
                app.logger.error(f'OwnerOf_Error on {domain} - Hash {payload[domain]["hash"]}')
                fails.append(domain)
            else:
                payload[domain]['owner'] = str(owner)

    # fails = fail_queue(fails, contract_instance, payload)
    
    app.logger.info(f"Domain metadata aquired...")
    app.logger.info(f'Fail Total {len(fails)} - Fail Queue {fails}')

    return payload


# def fail_queue(fail_que, contract, payload) -> list:
#     failed = []
#     for domain in fail_que:
#         try:
#             # Get domain expiration.
#             expires = contract.nameExpires(int(payload[domain]['hash']))
#             payload[domain]['expiration'] = expires
#         except(Exception) as e:
#             app.logger.error(f'NameExpires_Error on {domain}. Hash: {payload[domain]["hash"]}')
#             failed.append(domain)

#         try:
#             # Get domain owner.
#             owner = contract.ownerOf(int(payload[domain]['hash']))
#             payload[domain]['owner'] = owner
#         except(ContractLogicError) as e: # require(expiries[tokenId] > block.timestamp);
#             payload[domain]['owner'] = app.config['ENS_GRACE_AUCTION']
#             app.logger.error(f'OwnerOf_Error on {domain} - Hash {payload[domain]["hash"]}')
#             failed.append(domain)
#     return failed