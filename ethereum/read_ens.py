import requests
import json
import subprocess
import copy
from web3 import Web3
from typing import Dict, List
from datetime import datetime
from ethereum._base import Web3_Base#, app
from web3.exceptions import TimeExhausted, ContractLogicError
from backend.utils.utils import (
    app,
    post_to_db,
    apply_hashes_to_payload
)
from graphql.main import (
  make_graphql_request,
)
from backend.models.models import Domains
from graphql.queries import (
#   DOMAIN_ECO,
#   REGISTRATIONS,
  DOMAIN_OWNER,
  DOMAIN_OWNER_BATCH
)
# import pdb; pdb.set_trace()


# Very upstread. changes to this need to be throught about a little
def ens_claw(payload: Dict['str', dict] = None) -> Dict['str', dict]:
    '''
    Gathers owner, expiration, & availability data 
    on domains.
    Payload structure is outlined in watchlists/watch_clean.json
    '''
    w3_obj = Web3_Base()
    payload_copy = copy.deepcopy(payload)
    fails = []

    batched_graphql_calls = ''

    ## Load abi from https://etherscan.io/address/0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85#code
    abiFile = json.load(open('./ethereum/abis/ENS_Base_Registrar.json'))
    abi = abiFile['abi']
    base_registrar_contract = w3_obj.w3.eth.contract(
        abi=abi,
        address=app.config["ENS_BASE_REGISTRAR_MAINNET"],
    )

    app.logger.info(f"Gathering metadata on {len(payload_copy.keys())} domains...")

    # Iterate through all domains.
    for domain in payload_copy.keys():
        url = DOMAIN_OWNER_BATCH.replace('labelName:"_NAME"', f'labelName:"{str(domain)}"').replace('_HASH', f'H{payload[domain]["hash"]}')
        batched_graphql_calls += url

        # Get domain name.
        payload[domain]['name'] = str(domain)

        try: # Get domain availability.
            avail = base_registrar_contract.functions.\
                    available(int(payload[domain]['hash'])).call()
            payload[domain]['available'] = bool(avail)
        except(Exception) as e:
            app.logger.error(f'available on {domain} - Hash {payload[domain]["hash"]}')
            payload[domain]['available'] = False

        try: # Get domain expiration.
            expires = base_registrar_contract.functions.\
                        nameExpires(int(payload[domain]['hash'])).call()
        except(Exception) as e:
            app.logger.error(f'NameExpires_Error on {domain} - Hash {payload[domain]["hash"]}')
            payload[domain]['expiration'] = 'null'
            fails.append(domain)
        else: # From int timestamp to datetime.datetime object.
            # Converts expire TS into str DT -> 2122-01-14 01:12:19+00:00
            payload[domain]['expiration'] = datetime.fromtimestamp(expires) if expires != 0 else 'null'

        try: # Get domain owner.
            owner = base_registrar_contract.functions.\
                    ownerOf(int(payload[domain]['hash'])).call()
        except(ContractLogicError) as e: # require(expiries[tokenId] > block.timestamp); IE In Grace or Expired
            app.logger.error(f'OwnerOf_Error on {domain} - ' \
                            f'Hash {payload[domain]["hash"]} - ')
            fails.append(domain)
            # batch calling graphql for owners, sent to none till then.
            payload[domain]['owner'] = None
        else:
            payload[domain]['owner'] = str(owner).lower()
    
    batched_graphql_calls = insert_str(batched_graphql_calls, '{', 1)
    batched_graphql_calls = insert_str(batched_graphql_calls, '}', -1)
    batched_graphql_calls = batched_graphql_calls.replace('\n\n\n\n', '\n')
    resp = requests.post(url=app.config["GRAPHQL_ENS_URL"], json={"query": batched_graphql_calls})
    data = resp.json()

    for domain in payload_copy.keys():
        payload[domain]['owner'] = data['data'][f"H{payload[domain]['hash']}"][0]['registrant']['id']

    app.logger.info(f"Domain metadata aquired...")
    app.logger.info(f'Fail Total {len(fails)} - Fail Queue {fails}')

    return payload

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

def ens_claw_update_domains(domains):
    w3_obj = Web3_Base()

    abiFile = json.load(open('./ethereum/abis/ENS_Base_Registrar.json'))
    abi = abiFile['abi']
    base_registrar_contract = w3_obj.w3.eth.contract(
        abi=abi,
        address=app.config["ENS_BASE_REGISTRAR_MAINNET"],
    )

    for domain in domains:
        print(f"Updating {domain.name} ...")
        try: # Get domain owner.
            owner = base_registrar_contract.functions.\
                    ownerOf(int(domain.hash)).call()
            owner = str(owner)
        except(ContractLogicError) as e: # require(expiries[tokenId] > block.timestamp); IE In Grace or Expired
            app.logger.error(f'OwnerOf_Error on {domain.name} - Hash {domain.hash}')
            owner = get_owner_graphql(domain.name)

        try: # Get domain availability.
            avail = base_registrar_contract.functions.\
                    available(int(domain.hash)).call()
            avail = bool(avail)
        except(Exception) as e:
            app.logger.error(f'available on {domain.name} - Hash {domain.hash}')
            avail = False

        try: # Get domain expiration.
            expires = base_registrar_contract.functions.\
                        nameExpires(int(domain.hash)).call()
        except(Exception) as e:
            app.logger.error(f'NameExpires_Error on {domain.name} - Hash {domain.hash}')
            expires = None
        else: # From int timestamp to datetime.datetime object.
            # Converts expire TS into str DT -> 2122-01-14 01:12:19+00:00
            expires = datetime.fromtimestamp(expires) if str(expires).lower() != 'null' else None

        times = Domains.get_times_and_status(_expiration=expires.strftime(app.config['DATETIME_STR_FORMAT']))
        domain.owner = owner.lower()
        domain.available = avail
        domain.expiration = expires if expires != 'null' else 'NULL'
        domain.auction = times['auction']
        domain.grace = times['grace']
        domain.status = times['status']

        post_to_db(data=domain)


def get_premium(domain_name: str = None, years: int = 1):
    '''
    Returns premium of a domain in auction in ETH.
    '''
    w3_obj = Web3_Base()

    abiFile = json.load(open('./ethereum/abis/ETH_Registrar_Controller.json'))
    abi = abiFile['abi']
    eth_registrar_contract = w3_obj.w3.eth.contract(
        abi=abi,
        address=app.config["ENS_ETH_REGISTRAR_CONTROLLER_MAINNET"],
    )

    # Returns premium cost only, ensure domain is in auction when called.
    fee = eth_registrar_contract.functions.rentPrice(domain_name, int(years)).call()
    eth_fee = w3_obj.w3.fromWei(fee, 'ether')
    return eth_fee


def get_reverse_record(addresses: List[str] = None):
    '''
    Returns reverse record, ens domain set to address.
    '''
    import time
    start_time = time.time()

    # If addresses is not a list, return.
    if not isinstance(addresses, list):
        return {'error': 'addresses must be a list of string addresses'}

    cleaned = []
    records = {}
    for address in addresses:
        try:
            clean = address.replace('\n',  '').replace("'", "").replace('"', "").strip().replace('null', '').lower()
            clean = Web3.toChecksumAddress(clean)
            cleaned.append(clean)
        except Exception as error:
            pass

    app.logger.info(f'[ACTION] Cleaned addresses: {cleaned} ...')

    if len(cleaned) > 0:
        w3_obj = Web3_Base()

        abiFile = json.load(open('./ethereum/abis/ENS_Reverse_Records.json'))
        abi = abiFile['abi']
        ens_reverse_records_contract = w3_obj.w3.eth.contract(
            abi=abi,
            address=app.config["ENS_REVERSE_RECORDS_MAINNET"],
        )
    else:
        return {'error': 'must supply at least 1 address'} 

    # Get reverse records from ens contract.
    rr = ens_reverse_records_contract.functions.getNames(cleaned).call()

    # Map cleaned addresses to their reverse record.
    for index, clean in enumerate(cleaned):
        try:
            if (rr[index][:-4] != None and rr[index][:-4] != ''):
                records[clean.lower()] = (rr[index][:-4]).lower()
            else:
                records[clean.lower()] = None
            app.logger.info(f'Set RR for address {clean} to {rr[index][:-4]} ...')
        except Exception as error:
            records[clean] = None
            app.logger.warning(f'No RR for address: {clean}...')

    # records['time'] = time.time() - start_time
    data = {'reverse_records': records}
    return data


def get_owner_graphql(domain_name: str = None):
    '''
    Some domains have never had an owner because they have
    never been minted.
    '''
    try:
        resp = make_graphql_request('DOMAIN_OWNER', domain_name)
        owner = resp['data']['data']['registrations'][0]['registrant']['id']
        app.logger.info(f'Owner found from graphql query - {owner} ')
        if owner == []:
            return None
        else:
            return owner.lower()
    except Exception as error:
        app.logger.error(f'get_owner_graphql error: {error}')
        return app.config["ENS_BASE_REGISTRAR_MAINNET"]
