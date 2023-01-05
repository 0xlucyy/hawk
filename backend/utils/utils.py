from datetime import datetime
import idna
import json
import csv
import unicodedata
from typing import Tuple
from MySQLdb import _mysql
from app import app, db
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from backend.utils.exceptions import (
    DatabaseError
)
from web3 import (
    Web3
)
from web3.exceptions import (
    TimeExhausted,
    # ContractLogicError
)
# import pdb; pdb.set_trace()


def BASIC_TRANSACTION(w3: Web3 = None, address: str = None) -> dict:
    print(f"Gas price: {w3.fromWei(w3.eth.gas_price, 'gwei')}")
    print(f"Max Priority fee per gas: {w3.fromWei(w3.eth.max_priority_fee, 'gwei')}")
    print(f"From: {address}")
    print(f"Nonce: {w3.eth.get_transaction_count(address)}")

    return {
        'nonce': w3.eth.get_transaction_count(address),
        'from': address,
        'maxFeePerGas': (w3.eth.gas_price * 2), #w3.toWei(1, 'gwei'),
        'maxPriorityFeePerGas': (w3.eth.max_priority_fee * 1.5), # w3.toWei(1, 'gwei'),
    }

'''
Returns:
    (Bool, Str) : True/False, Either err msg or transaction hash
'''
def SIGN_SEND_WAIT(w3: Web3 = None, transaction: dict = None, FLOWERS_PRIV_KEY: str = None) -> Tuple[bool, str]:
    signed_tx = w3.eth.account.sign_transaction(transaction, FLOWERS_PRIV_KEY)

    try:
        tx_hash = w3.eth.send_raw_transaction(transaction=signed_tx.rawTransaction)
        print(f'Transaction hash: {tx_hash.hex()}')
    except ValueError as VE:
        print(f'ERROR - value error')
        print(f'Code: {VE.args[0]["code"]}')
        print(f'Message: {VE.args[0]["message"]}')
        return (False, VE.args[0]["message"])
    except Exception as err:
        print(f"err: {err}")
        print(f"err.args: {err.args}")
        print(f"err.args: {err.args[0]}")
        return (True, err.args[0]["message"])

    try:
        tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash)
        print(f'Transaction receipt: {tx_receipt["transactionHash"].hex()}')
    except TimeExhausted as TE:
        print('ERROR - time exhausted')
        print(f'Code: {TE.args[0]["code"]}')
        print(f'Message: {TE.args[0]["message"]}')
        return (False, TE.args[0]["message"])
    except Exception as err:
        print(f"err: {err}")
        print(f"err.args: {err.args}")
        print(f"err.args: {err.args[0]}")
        return (True, err.args[0]["message"])

    return (True, tx_receipt)

def INCREASE_GAS(transaction: dict, percentage: float = app.config["GAS_INCREASE"]):
    transaction['maxFeePerGas'] = int((transaction['maxFeePerGas'] * \
        percentage) + transaction['maxFeePerGas'])
    transaction['maxPriorityFeePerGas'] = \
        int((transaction['maxPriorityFeePerGas'] * percentage) + \
        transaction['maxPriorityFeePerGas'])
    return transaction

def get_tx_pool_content(w3: Web3 = None):
    return w3.geth.txpool.content()

def get_tx_pool_status(w3: Web3 = None):
    return w3.geth.txpool.status()

def post_to_db(data=None, just_commit=False):
    try:
        if(just_commit == False):
            db.session.add(data)
        db.session.commit()
    except IntegrityError as IE:
        db.session.rollback()
        app.logger.error(f"{data} not inserted into db.")
        raise IE

def is_db_live():
    try:
        conn = db.engine.execute(text("SELECT 1"))
        return conn.connection._still_open_and_dbapi_connection_is_valid
    except:
        raise DatabaseError

# tilde_identifier('drügonñátest')
def tilde_identifier(word : str = None):
    '''
        Answers, does word contain any special characters.
    '''
    if any(tilde in word for tilde in app.config['SPANISH_TILDES']):
        # print(f"Tilde found in {word}.")
        return True
    return False

def remove_accents(word):
    '''
        Return word without special characters.
    '''
    only_ascii = (unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore')).decode("utf-8")
    # print(f"Copied {word} into {only_ascii}")
    return only_ascii

def apply_hashes_to_payload(payload : dict = None):
    '''
    Adds hash values to payload object. Hash values are
    in csv format in default WATCH_LOCATION ie /watchlists/watch_clean.csv
    '''
    with open(f"{app.config['WATCH_LOCATION']}.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            payload[row[0]] = {'hash': row[1]}
    if "" in payload.keys(): del payload['']
    return payload

def create_database():
    # establishing the connection
    db_connection = _mysql.connect(user=app.config['MYSQL_USERNAME'], password=app.config['MYSQL_PASSWORD'], host='127.0.0.1')

    # Doping database MYDATABASE if already exists.
    db_connection.query(f"DROP database IF EXISTS {app.config['MYSQL_DB']}")

    # Creating a database
    db_connection.query(f"CREATE database {app.config['MYSQL_DB']}")

    db_connection.query("SHOW DATABASES")
    results = db_connection.use_result()

    # #Closing the connection
    db_connection.close()

def stringify(attribute: object) -> str:
	'''
	Serializes attribute object into JSON formatted string.
	'''
	try:
		if isinstance(attribute, dict):
			value = json.dumps(attribute)
		elif isinstance(attribute, str):
			value = json.dumps(attribute)
			value = value.replace('"', "")
		return value
	except:
		return attribute

def domain_status(expiration, grace, auction):
    now = datetime.now()
    if expiration == None:
        return app.config["DOMAIN_STATUS_FREE"]

    if now < expiration: # Domain has not expired.
        return app.config["DOMAIN_STATUS_HODLING"]
    else: # domain is expired. Either in Free, in grace, or in auction.
        if now > auction: # Auction is over.
            return app.config["DOMAIN_STATUS_FREE"]
        else: # domain is expired. it is either in grace or in auction.
            if now > grace: # Grace period is over.
                return app.config["DOMAIN_STATUS_IN_AUCTION"]
            else: # Grace period is not over.
                return app.config["DOMAIN_STATUS_IN_GRACE"]
