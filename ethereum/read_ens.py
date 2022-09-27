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
    # account = w3.eth.account.privateKeyToAccount(LOCAL_PRIV_KEY)

    # truffleFile = json.load(open('./build/contracts/AvatarHistory.json'))
    truffleFile = json.load(open('./build/contracts/BaseRegistrarImplementation.json'))
    abi = truffleFile['abi']
    bytecode = truffleFile['bytecode']
    contract = w3_obj.w3.eth.contract(bytecode=bytecode, abi=abi)
    # import pdb; pdb.set_trace()
    
    ## DEPLOY
    # import pdb; pdb.set_trace()
    # construct_txn = contract.constructor(10000000000000000).\
    #     buildTransaction(BASIC_TRANSACTION(w3_obj.w3, account.address))
    # success, tx_receipt = SIGN_SEND_WAIT(w3_obj.w3, construct_txn, w3_obj.context.LOCAL_PRIV_KEY)

    # ## WRITE
    # contract_instance = w3_obj.w3.eth.contract(
    #     abi=abi, 
    #     address=w3_obj.context.ETH_REGISTRAR_CONTROLLER
    # )
    # construct_txn = contract_instance.functions.\
    #         makeCommitment('tesdfsdfsd', Web3.toChecksumAddress(account.address), '666'.encode('utf-8')).\
    #         buildTransaction(BASIC_TRANSACTION(w3_obj.w3, account.address))
    # result = SIGN_SEND_WAIT(w3_obj.w3, construct_txn, w3_obj.context.NORDSTREAM2_PRIV_KEY)
    # receipt = w3_obj.w3.eth.get_transaction_receipt('0x6ba2c2255d6d8f07cf1d10f5ab48c14c44b3968d201846bb2eed6e9224ea133b')

    ## READ
    # import pdb; pdb.set_trace()
    contract_instance = w3_obj.w3.eth.contract(abi=abi,
        address=app.config["ENS_BASE_REGISTRAR_MAINNET"],
        ContractFactoryClass=ConciseContract
    )
    
    import pdb; pdb.set_trace()
    avail = contract_instance.available(15768640270076878341175039412133896973600956267551796498581508331098277461878)
    # construct_txn = contract_instance.makeCommitment('tesdfsdfsd', Web3.toChecksumAddress(account.address), bytes(666)).buildTransaction(BASIC_TRANSACTION(w3_obj.w3, account.address))
    print('Contract value: {}'.format(avail))

main()