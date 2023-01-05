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
# import pdb; pdb.set_trace()


# Very upstread. changes to this need to be throught about a little
def ens_claw(payload: Dict['str', dict] = None) -> Dict['str', dict]:
    '''
    Gathers owner, expiration, & availability data 
    on domains.
    '''
    w3_obj = Web3_Base()
    payload_copy = copy.deepcopy(payload)
    fails = []

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
            payload[domain]['owner'] = get_owner_graphql(domain)
        else:
            payload[domain]['owner'] = str(owner)
    
    app.logger.info(f"Domain metadata aquired...")
    app.logger.info(f'Fail Total {len(fails)} - Fail Queue {fails}')

    return payload


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
        domain.owner = owner
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
    # If addresses is not a list, return.
    if not isinstance(addresses, list):
        return {'error': 'addresses must be a list of string addresses'}

    w3_obj = Web3_Base()

    abiFile = json.load(open('./ethereum/abis/ENS_Reverse_Records.json'))
    abi = abiFile['abi']
    ens_reverse_records_contract = w3_obj.w3.eth.contract(
        abi=abi,
        address=app.config["ENS_REVERSE_RECORDS_MAINNET"],
    )

    cleaned = []
    records = {}
    for address in addresses:
        try:
            clean = address.replace('\n',  '').replace("'", "").replace('"', "")
            clean = Web3.toChecksumAddress(clean.strip())
            cleaned.append(clean)
        except Exception as error:
            pass

    # Get reverse records from ens contract.
    rr = ens_reverse_records_contract.functions.getNames(cleaned).call()

    for index, clean in enumerate(cleaned):
        # Clean csv file & normalization placeholder.
        f = open(f"{app.config['WATCH_LOCATION']}.csv", "w+")
        f.close()
        normalized_rr = {}

        try:
            # Plug into cmd reverse record without .eth end.
            get_hashes_cmd = f"node ethereum/normalize.js '{rr[index][:-4]}' >> watchlists/watch_clean.csv"
            # Run normalization on reverse record.
            subprocess.run(['sh', '-c', get_hashes_cmd])
            # Using this to scrap results from csv file.
            normalized_rr = apply_hashes_to_payload({})
            # Pair address with ens domain reverse record.
            records[clean] = list(normalized_rr.keys())[0]
        except Exception as error:
            records[clean] = None
            app.logger.error(f"error in get_reverse_record: {error}")

    data = {'reverse_records': records}
    return data


def get_owner_graphql(domain_name: str = None):
    '''
    Some domains have never had an owner because they have
    never been minted.
    '''
    try:
        app.logger.info(f'Querying graphql for owner on domain: {domain_name}...')
        resp = make_graphql_request('DOMAIN_OWNER', domain_name)
        owners = resp['data']['data']['domains']
        if owners == []:
            return "NEVER_BEEN_MINTED"
        else:
            return owners[0]['owner']['id']
    except Exception as error:
        app.logger.error(f'get_owner_graphql error: {error}')
        return 'ERROR'
