import requests
import json
import time

# import subprocess
import copy
from web3 import Web3
from typing import Dict, List
from datetime import datetime
from ethereum._base import Web3_Base#, app
from web3.exceptions import TimeExhausted, ContractLogicError
from backend.utils.utils import (
    app,
    post_to_db,
    insert_str
)
from backend.models.models import Domains
# TheGraph ENS subgraph sectio
from graphql.queries import (
#   DOMAIN_OWNER,
  DOMAIN_OWNERS_BATCH,
  DOMAIN_METADATA_BATCH,
  DOMAIN_METADATA
)
from graphql.main import (
  make_graphql_request,
)
# import pdb; pdb.set_trace()


# Very upstread. changes to this need to be throught about
def test(payload: Dict['str', dict] = None) -> Dict['str', dict]:
  '''
  Gathers 
  '''
  payload_copy = copy.deepcopy(payload)
  batched_graphql_calls = ''
  batched_list = []
  all_data = {}
  batchIndex = 0

  app.logger.info(f"Gathering metadata on {len(payload_copy.keys())} domains...")

  # Batch all queries into groups of 300, then add those groups to a list.
  for domain in payload_copy.keys():
    ''' 
        subgraph cant handle more than 300 queries in one request.
        Add the 300 batched requests, and start working on the next
        300.
    '''
    if batchIndex == 300:
      batched_list.append(copy.deepcopy(batched_graphql_calls))
      batched_graphql_calls = ''
      batchIndex = 0

    # Prepare the URL and add to batched calls.
    url = DOMAIN_METADATA_BATCH.replace('labelName:"_NAME"', f'labelName:"{str(domain)}"').replace('_HASH', f'H{payload[domain]["hash"]}')
    batched_graphql_calls += url
    batchIndex += 1

  # Append last query calls, less than 300 in this batch.
  if batched_graphql_calls != '':
    batched_list.append(copy.deepcopy(batched_graphql_calls))

  app.logger.info(f"[INFO] Making a total of {len(batched_list)} batched requests to thegraph ens subgraph ...")


  # Add outter brackets and normalize \n's, then make bulk query request.
  index = 0
  for batched_query in batched_list:
    batched_query = insert_str(batched_query, '{', 1)
    batched_query = insert_str(batched_query, '}', -1)
    batched_query = batched_query.replace('\n\n\n\n', '\n')
    app.logger.info(f"[ACTION] Making batched ens subgraph request #{index} ...")
    resp = requests.post(url=app.config["GRAPHQL_ENS_URL"], json={"query": batched_query})
    data = resp.json()
    index += 1

    if 'error' not in data.keys():
        app.logger.info(f"[INFO] Status: {resp.status_code} ...")
        all_data.update(copy.deepcopy(data['data']))
    else:
        app.logger.error(f"[ERROR] batched query failed. Error: {data}")

    app.logger.info(f"[INFO] Sleeping for 5 seconds ...")
    time.sleep(5)


  # Access respnse data from graphql ens subgraph.
  for domain in payload_copy.keys():
    try:
      # Set domain name.
      payload[domain]['name'] = str(domain)
      
      # Set domain expiration & owner.
      if all_data[f"H{payload[domain]['hash']}"] != []:
        owner = all_data[f"H{payload[domain]['hash']}"][0]['registrant']['id']
        expires = int(all_data[f"H{payload[domain]['hash']}"][0]['expiryDate'])
        payload[domain]['owner'] = owner
        payload[domain]['expiration'] = datetime.fromtimestamp(expires) if expires != 0 else 'null'
      else:
        payload[domain]['owner'] = app.config["ENS_BASE_REGISTRAR_MAINNET"]
        payload[domain]['expiration'] = 'null'
      
      app.logger.info(f"[INFO] Domain: {domain} Owner: {payload[domain]['owner']} Expires: {payload[domain]['expiration']} ...")
    except Exception as err:
      app.logger.error(f"[ERROR] Setting owner from graphql. Error: {err}")

  app.logger.info(f"Domain metadata aquired...")
  return payload


# def siwe():
#   from siwe import SiweMessage
#   from siwe.siwe import VerificationError, InvalidSignature, MalformedSession, DomainMismatch, ExpiredMessage, MalformedSession, NonceMismatch, NotYetValidMessage
#   from dateutil.relativedelta import relativedelta
#   import random
#   web3 = Web3_Base()

#   account = web3.w3.eth.account.privateKeyToAccount(app.config["PRIV_KEY_ONE"])

#   try:
#     # addr = account.address
#     addr = '0xc342287e1059265016e0ec756971d44Ce85566CB'
#     now_dt = datetime.now()
#     iso_dt = now_dt.isoformat()
#     expiration = (now_dt + relativedelta(days=1))
#     exp_dt = expiration.isoformat()

#     message: SiweMessage = SiweMessage(message={
#       "domain": "127.0.0.1:7545",
#       "address": addr,
#       "statement": "Sign in with Ethereum to the app.",
#       # 'uri': 'http://geth.dappnode:8545',
#       'uri': 'http://127.0.0.1:7545',
#       "version": '1',
#       'chain_id': '1337',
#       'issued_at': iso_dt,
#       'expiration_time': exp_dt,
#       'nonce': random.randrange(000000000000, 999999999999)
#       }
#     )
#     import pdb; pdb.set_trace()
#     message.prepare_message()
#     # signed_message = web3.w3.eth.account.sign_message(message, private_key=app.config["PRIV_KEY_ONE"])
#     signed_message = web3.w3.eth.account.sign_message(message, private_key=app.config["PRIV_KEY_TWO"])
#     message.verify(signature=addr)
#   except ValueError:
#       # Invalid message
#       print("Authentication attempt rejected. Invalid message.")
#   except NotYetValidMessage:
#       # The message is not yet valid
#       print("Authentication attempt rejected. The message is not yet valid.")
#   except ExpiredMessage:
#       # The message has expired
#       print("Authentication attempt rejected. The message has expired.")
#   except DomainMismatch:
#       print("Authentication attempt rejected. Domain mismatch.")
#   except NonceMismatch:
#       print("Authentication attempt rejected. The nonce is not the expected one.")
#   except MalformedSession as e:
#       # e.missing_fields contains the missing information needed for validation
#       print("Authentication attempt rejected. Missing fields")
#   except InvalidSignature:
#       print("Authentication attempt rejected. Invalid signature.")
#   except VerificationError:
#       # VerificationError
#       print("Authentication attempt rejected. Verification Error.")
# siwe()
