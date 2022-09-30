import sys
import unicodedata
from typing import Tuple
from app import app, db
from sqlalchemy.sql import text
from backend.utils.exceptions import (
    DatabaseError
)
from web3 import (
    Web3
)
from web3.exceptions import (
    TimeExhausted,
    ContractLogicError
)

# import pdb; pdb.set_trace()



def BASIC_TRANSACTION(w3: Web3 = None, address: str = None) -> dict:
    import pdb; pdb.set_trace()

    print(f"Gas price: {w3.fromWei(w3.eth.gas_price, 'gwei')}")
    print(f"Max Priority fee per gas: {w3.fromWei(w3.eth.max_priority_fee, 'gwei')}")
    print(f"From: {address}")
    print(f"Nonce: {w3.eth.get_transaction_count(address)}")

    # import pdb; pdb.set_trace()
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
    # import pdb; pdb.set_trace()

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

def post_to_db(data):
# def post_to_db(db, data):
    db.session.add(data)
    db.session.commit()
    app.logger.info(f"{data} inserted into db.")

# def is_db_live(db):
def is_db_live():
    try:
        conn = db.engine.execute(text("SELECT 1"))
        return conn.connection._still_open_and_dbapi_connection_is_valid
    except:
        raise DatabaseError

def normalize_file(file = None):
    '''
        Takes an uncleaned file and produces a cleaned &
        normalized file.
    '''
    # import pdb; pdb.set_trace()
    if file == None:
        file = sys.argv[1]
    # file = 'test'

    # Read from uncleaned file.
    with open(f"{app.config['DOMAIN_WATCH_LIST_PATH']}/{file}.txt", 'r') as f:
        lines = f.readlines()

    clean = []
    for line in lines:
        line = line.lower()
        clean.append(line.replace('\n', ""))
    
    # If word is special, create non-special copy.
    for word in clean:
        if tilde_identifier(word) == True:
            non_tilde_copy = remove_accents(word)
            clean.append(non_tilde_copy.replace('\n', ""))

    # Sort & dedup.
    clean.sort()
    clean = list(dict.fromkeys(clean))
    clean.pop(0) # Remove whitespace entry
    
    # Produces cleaned human text file.
    f = open(f"{app.config['DOMAIN_WATCH_LIST_PATH']}/{file}-{app.config['CLEAN_LIST']}.txt", 'w')
    for word in clean:
        f.write(word.replace(' ', ''))
        f.writelines('\n')

    f.close()


# tilde_identifier('drügonñátest')
def tilde_identifier(word : str = None):
    '''
        Answers, does word contain any special characters.
    '''
    if any(tilde in word for tilde in app.config['SPANISH_TILDES']):
        print(f"Tilde found in {word}.")
        return True
    return False


def remove_accents(word):
    '''
        Return word without special characters.
    '''
    only_ascii = (unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore')).decode("utf-8")
    print(f"Copied {word} into {only_ascii}")
    return only_ascii

# normalize_file()