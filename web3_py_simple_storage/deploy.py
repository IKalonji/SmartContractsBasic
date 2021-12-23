import os
from solcx import compile_standard
from json import dump
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

#Compile Solidity code

compiled_solidity = compile_standard({
    "language": "Solidity",
    "sources": {
        "SimpleStorage.sol": {
            "content": simple_storage_file
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
               "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"] 
                }
            }
        },
    },
)

with open("compiled_solidity.json", "w") as file:
    dump(compiled_solidity, file)

#get bytecode
bytecode = compiled_solidity["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
#get abi
abi = compiled_solidity["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#Connect to blockchain
_web3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/ee6496833cbb402a82fc2483c2bff17c"))

chain_id = 42

my_addr = "0xB45b197cA2d6A3F8F1EFdA5Fe8509D43D93c6295"

key = os.getenv("PRIVATE_KEY")

SimpleStorage = _web3.eth.contract(abi=abi, bytecode=bytecode)

nonce = _web3.eth.getTransactionCount(my_addr)

#create transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": _web3.eth.gas_price,
        "chainId": chain_id,
        "from": my_addr,
        "nonce": nonce
    }
)

signed_txn = _web3.eth.account.sign_transaction(transaction, key)

#send transaction

tx_hash = _web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = _web3.eth.wait_for_transaction_receipt(tx_hash)


#work with contract

simple_storage = _web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": _web3.eth.gas_price,
        "chainId": chain_id,
        "from": my_addr,
        "nonce": nonce + 1
    }
)

sign_store_txn = _web3.eth.account.sign_transaction(store_transaction, key)

store_transaction_hash = _web3.eth.send_raw_transaction(sign_store_txn.rawTransaction)

store_transaction_receipt = _web3.eth.wait_for_transaction_receipt(store_transaction_hash)

print(simple_storage.functions.retrieve().call())




