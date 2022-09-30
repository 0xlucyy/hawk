import json
# from web3 import Web3
from backend.utils.utils import (
    BASIC_TRANSACTION,
    SIGN_SEND_WAIT,
    Web3,
    app
)
from ethereum._base import Web3_Base#, app
from web3.exceptions import TimeExhausted
from web3.contract import ConciseContract

# import pdb; pdb.set_trace()


def main():
    w3_obj = Web3_Base()

    account = w3_obj.w3.eth.account.privateKeyToAccount(app.config["NORDSTREAM2_PRIV_KEY"])

    truffleFile = json.load(open('./build/contracts/BaseRegistrarImplementation.json'))
    abi = truffleFile['abi']
    bytecode = truffleFile['bytecode']
    contract = w3_obj.w3.eth.contract(bytecode=bytecode, abi=abi)

    ## READ
    # import pdb; pdb.set_trace()
    contract_instance = w3_obj.w3.eth.contract(abi=abi,
        address=app.config["ENS_BASE_REGISTRAR_MAINNET"],
        ContractFactoryClass=ConciseContract
    )
    
    import pdb; pdb.set_trace()
    avail = contract_instance.available(15768640270076878341175039412133896973600956267551796498581508331098277461878)
    if not avail:
        expires = contract_instance.nameExpires(15768640270076878341175039412133896973600956267551796498581508331098277461878)

    # construct_txn = contract_instance.makeCommitment('tesdfsdfsd', Web3.toChecksumAddress(account.address), bytes(666)).buildTransaction(BASIC_TRANSACTION(w3_obj.w3, account.address))
    print('Contract value: {}'.format(avail))

main()