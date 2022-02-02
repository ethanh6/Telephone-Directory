# Web3.py demo 
Learning Web3.py will clarify everything behind the scene when using frameworks like Brownie.

- IDE: VS Code, Vim, etc.
- Ganache
    1. a local simulated blockchain environment for development purpose (similar to Rinkeby testnet, but local)
    2. has both GUI (good user interface to check the local blockchain state) and CLI, `ganache-cli` (that brownie uses)
        1. install ganache-cli: install Nodejs and Yarn
    3.  also has simulated accounts with balance, address, private key and mnemonics

### File Structure

- `TelephoneDirectory.sol` : all contracts code here
- `deploy.py` : deploy python script using Web3.py
- `.env` : store all environment variables (testing addresses and private keys)
- `.gitignore` 
    - make sure to put `.env` 

### Use environment variable to set private key: `.env`

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


### To connect to a real blockchain (mainnet or testnet)

1. use blockchain endpoint provided by centralized services
    - Infura, alchemy → these services will give you an endpoint (RPC server address) to the blockchain
    - only need to change the config in step 3.b (RPC server address, Network ID and account address)
2. run your own blockchain node
    - go-ethereum (geth)

- To check and see the actual transaction on either mainnet or testnet → [etherscan.io](http://etherscan.io)