# Web3.py demo 
Learning Web3.py will clarify everything behind the scene when using frameworks like Brownie.

- IDE: VS Code, Vim, etc.
- Ganache
    1. a local simulated blockchain environment for development purpose (similar to Rinkeby testnet, but local)
    2. has both GUI (good user interface to check the local blockchain state) and CLI, `ganache-cli` (that brownie uses)
        1. install ganache-cli: install Nodejs and Yarn
    3.  also has simulated accounts with balance, address, private key and mnemonics

### File Structure

- `SimpleStorage.sol` : all contract code here
- `deploy.py` : deploy python script using Web3.py
- `.env` : store all environment variables
    - `export PRIVATE_KEY=0x123abc...`
    - make sure to set `.gitignore` with `.env` in it

### Use environment variable to set private key

1. `export PRIVATE_KEY=0xabcde...`  (need to set up `.gitignore` - it’s volatile and dangerous, not recommended)
2. use `python-dotenv` package to pull the env var directly in python.

### deploy.py → details about the steps for deploying a contract on chain

1. Read contract file
2. Compile contract file (`pip install py-solc-x`) 
3. Connect to Ganache
    1. require bytecode and ABI 
    2. Connect to Ganache 
        - RPC server: <ID address>:<port>
        - Network ID: 1337 (for Ganache)
        - An account address to deploy from (with private key)
4. Create the contract in Python
5. Get nonce (for the latest transaction)
6. Deploy to blockchain → build a transaction cause we are making a state change to the blockchain
    1. Build the contract deploy transaction
    2. Sign the transaction
    3. Send the transaction
    4. Wait for the transaction to be mined (confirmation) and see the transaction receipt.
7. Interact and work with the deployed contract
    - ALWAYS requires 2 things: `Contract Address` and `ABI`
    - 2 ways of interaction
        1. `Call`: does NOT make any state changes; only get return value; only get info from blockchain e.g., view functions
        2. `Transact`:  will attempt to (and may or may not) make state changes to the blockchain 
    - Making a transaction is similar to deploy a contract (since they are both making state changes to the blockchain), so it also follows the steps from 6.a to 6.d

### Deploy.py

```python
import json, os
from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

# 1. Read Contract File
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")

# download and install precompiled solc (solidity compiler) binary
install_solc("0.6.0")

# 2. Compile the contract file
compiled_sol = compile_standard(
    {
        "language": "Solidity", 
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },

		# choose the version of the compiler
    solc_version="0.6.0",
)

# compiled_sol will be a json file will all the data (abi, metadata, bytecode, sourcemap)
# about the compiled file. we dump it into compiled_code.json 
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# 3.a get bytecode and ABI
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"])["output"]["abi"]

# Foe connecting to Rinkeby testnet
# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4

# 3.b connect to Ganache (or mainnet, or testnet)
w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545")) # RPC provider
chain_id = 1337
my_address = "0xdbB4A708755dfD59f9c4b100B2BE23a6d2EB7D57"  # the contract are going to be deployed from this address & private key
# private_key = "0xffdd7a010ab8c089d95a9c2ff24e75b21744b5db26c3cd66d14f8e91c46afcc4"  -> private key hard coded, bad

# alternative: access private key in Env Var, need to load it first by using load_dotenv()
load_dotenv()
private_key = os.getenv("PRIVATE_KEY")

# 4. Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# 5. Get the latest transaction for the Nonce
nonce = w3.eth.getTransactionCount(my_address)

# 6.a Build the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# 6.b Sign the transaction with private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")

# 6.c Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# 6.d Wait for the transaction to be confirmed (mined) and for the receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

 
# 7. Interact and working with deployed contracts, requires Contract Address and ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# this is function call, does not make any state change
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

# build transaction
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,  # this can be set to whatever
        "from": my_address,
        "nonce": nonce + 1,
    }
)

# sign transaction
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

	# send transaction
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")

# wait for confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
print(simple_storage.functions.retrieve().call())
```

### To connect to a real blockchain (mainnet or testnet)

1. use blockchain endpoint provided by centralized services
    - Infura, alchemy → these services will give you an endpoint (RPC server address) to the blockchain
    - only need to change the config in step 3.b (RPC server address, Network ID and account address)
2. run your own blockchain node
    - go-ethereum (geth)

- To check and see the actual transaction on either mainnet or testnet → [etherscan.io](http://etherscan.io)