import json, os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()

# 1. Read Contract File
with open("./TelephoneDirectory.sol", "r") as file:
    telephone_directory_file = file.read()
    
# download and install precompiled solc (solidity compiler) binary
SOLC_VERSION = "0.6.0"
print("Installing...")
install_solc(SOLC_VERSION)

# 2. Compile the contract file
compiled_sol = compile_standard(
    {
        "language": "Solidity", 
        "sources": {"TelephoneDirectory.sol": {"content": telephone_directory_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version=SOLC_VERSION,  # choose the version of the compiler
)

# compiled_sol will be a json file with all the data (abi, metadata, bytecode, sourcemap)
# about the compiled file. we dump it into compiled_code.json 
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# 3.a get bytecode and ABI
bytecode = compiled_sol["contracts"]["TelephoneDirectory.sol"]["TelephoneDirectory"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["TelephoneDirectory.sol"]["TelephoneDirectory"]["metadata"])["output"]["abi"]

# Foe connecting to Rinkeby testnet
# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4

# 3.b connect to Ganache (or mainnet, or testnet)
w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545")) # RPC provider
chain_id = 1337

# the contract are going to be deployed from this address & private key
# my_address = "0xDc262d10f6eDA62021CE0dF227181a86F9880eb5" 
# private_key = "0xffdd7a010ab8c089d95a9c2ff24e75b21744b5db26c3cd66d14f8e91c46afcc4"  -> private key hard coded, bad

# alternative: access private key in Env Var, need to load it first by using load_dotenv()
load_dotenv()
private_key = os.getenv("PRIVATE_KEY")
my_address = os.getenv("ADDRESS")

# 4. Create the contract in Python
TelephoneDir = w3.eth.contract(abi=abi, bytecode=bytecode)

# 5. Get the latest transaction for the Nonce
nonce = w3.eth.getTransactionCount(my_address)

# 6.a Build the transaction that deploys the contract
transaction = TelephoneDir.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# update nonce
nonce += 1

# 6.b Sign the transaction with private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")

# 6.c Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# 6.d Wait for the transaction to be confirmed (mined) and for the receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Well done! Contract deployed to {tx_receipt.contractAddress}")

print()


# 7. Interact with a deployed contracts (requires contract Address and contract ABI)
print("Interacting with the contract")
telephone_directory = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# this is function call, does not make any state change
print(f"Initial Amount of People = {telephone_directory.functions.get_total_people_number().call()}")

print("Please add a People!")
name = str(input("Enter name: "))
number = int(input("Enter number: "))

# build transaction, this makes state changes to the blockchain
print("Building transaction...")
tx = telephone_directory.functions.add_people(name, number).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,  # this can be set to whatever
        "from": my_address,
        "nonce": nonce,
    }
)

# sign transaction
print("Signing transaction...")
signed_tx = w3.eth.account.sign_transaction(
    tx, private_key=private_key
)

# send the signed transaction
print("Sending the signed transaction...")
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

print("Updating stored Value...")

# wait for confirmation
print("Waiting for the confirmation...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Transaction done! Tx hash: {tx_receipt.transactionHash.hex()}")


# this is function call, does not make any state change
print(f"Updated amount of People = {telephone_directory.functions.get_total_people_number().call()}")
print(f"Info or the new people = {telephone_directory.functions.get_info().call()}")