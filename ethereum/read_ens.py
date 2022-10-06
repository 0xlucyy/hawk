import json
import copy
from typing import Dict
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
    account = w3_obj.w3.eth.account.privateKeyToAccount(app.config["NORDSTREAM2_PRIV_KEY"])

    truffleFile = json.load(open('./build/contracts/BaseRegistrarImplementation.json'))
    abi = truffleFile['abi']
    bytecode = truffleFile['bytecode']
    contract = w3_obj.w3.eth.contract(bytecode=bytecode, abi=abi)

    contract_instance = w3_obj.w3.eth.contract(
        abi=abi,
        address=app.config["ENS_BASE_REGISTRAR_MAINNET"],
        ContractFactoryClass=ConciseContract
    )

    app.logger.info(f"Gathering metadata on {len(payload_copy.keys())} domains...")

    # Iterate through all domains.
    for domain in payload_copy.keys():
        # app.logger.info(f"Gathering metadata on {domain}...")
        avail = contract_instance.available(int(payload[domain]['hash']))
        payload[domain]['available'] = avail

        if avail == True: # Domain can be minted right now.
            payload[domain]['expiration'] = 0
            payload[domain]['owner'] = 'null'
        else: # Domain is either expiring, in grace, or being held.
            try:
                # Get domain expiration.
                expires = contract_instance.nameExpires(int(payload[domain]['hash']))
                payload[domain]['expiration'] = expires
            except(Exception) as e:
                app.logger.error(f'NameExpires_Error on {domain} - Hash {payload[domain]["hash"]}')
                fails.append(domain)

            try:
                # Get domain owner.
                owner = contract_instance.ownerOf(int(payload[domain]['hash']))
                payload[domain]['owner'] = owner
            except(ContractLogicError) as e: # require(expiries[tokenId] > block.timestamp); IE In Grace or Expired
                payload[domain]['owner'] = app.config['ENS_GRACE_AUCTION']
                app.logger.error(f'OwnerOf_Error on {domain} - Hash {payload[domain]["hash"]}')
                fails.append(domain)

    # fails = fail_queue(fails, contract_instance, payload)
    
    app.logger.info(f"Domain metadata aquired...")
    app.logger.debug(f'Fail Total {len(fails)} - Fail Queue {fails}')

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