## This script must be run on ETHEREUM testnet

### Info

Example of Smart contract association with location and prover:
- **1° Smart contract associated to 7H369F4W+Q8 location:** prover with DID 2 is the creator and his neighbours are 6, 50 and 51;
- **2° Smart contract associated to 7H369F4W+Q9 location:** prover with DID 8 is the creator and his neighbours are 9, 10 and 11.

The verifier has a balance, on Reach Devnet, equal to 1500 and sends 500 eth to both smart contracts.
Ther verifier will also verify all the proof and location inside the smart contracts.

## Main Features

- [Open Location Code](https://www.placekey.io/blog/google-maps-plus-codes-location-keys)
- Reach
- Python

##  Run

You have to [install Reach](https://docs.reach.sh/quickstart/) and start the docker. 
To run the **index.py** script, use:
- `pip install -r requirements.txt`
- `pip install --upgrade reach-rpc-client`
- `./reach rpc-run python3 -u ./index.py`

If you want to try the simulation use:
- `./reach rpc-run python3 -u ./startSimulation.py`

## How it works

- **index.rsh**: Smart Contract backend code;
- **index.py**: Frontend code (that interact with Smart Contract backend code);
- **startSimulation**: Simulation script that will call functions inside index.py to interact with Smart Contract.

Some functionalities of scripts; initial interactions between Deployer and Prover: 
<center><img src="img/interactionsScripts.png" width="75%" align="center"></center>

[Without Factory Contract]: Performance evaluation with Ethereum (x: accounts, y: seconds):
<center><img src="img/ethPerf.png" width="75%" align="center"></center>
Account 1° and 5° deploy new smart contract.

Outcome [not correct | fixed with the new version]:
<center><img src="img/terminalStartSimulation.png" width="75%" align="center"></center>

## If issues comes ...
Try with
- `./reach down`
- `./reach update`

## Test on Ganache:
- `REACH_CONNECTOR_MODE=ETH-live ETH_NODE_URI=http://host.docker.internal:7545 REACH_ISOLATED_NETWORK=1 ./reach rpc-run python3 -u startSimulation.py`

# Author
Michele Bonini
