from hashlib import new
from eth_account import Account
import secrets
from web3 import Web3
import time

#This script has been used to create new Ethereum accounts and send them some money.


# public key is the key - private key is the value
dict_private_public_key = {
    '0x34c17b647dDd4E38CDC2F5B38efd1F42681cB889': '0xf641b77d995ebade72e5a96f065232d9057284581e6b3ef6cbc194896ce606fa',
    '0xAc18Ec4c7f390663B179a7891f26247612654c8c': '0x833170377ef9e0cac6ae75989fed851279b723d12cfa880023adff5f341c8ab0', # 
    '0xF8f1AAcEDf0dBB07693f76e807e4EF9a96A6Aa9f': '0x9de62bf46a345f949b6e2f07088a626f07e84f7ca4269917188573a0b1d0be4b', # 
    '0x91EF6D0F7c12b5FF0c1F81DCFFAF1e30BF0F52D7': '0xc291f9aea360cc6d09a5bc071af3ee5e29a18bee02f4d39ed9f50633c7863eb1'
}

def newAccount():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    # print("Address:", acct.address)
    # print ("Private key:", private_key)
    print("'",private_key,"', #",acct.address)
    #dict_private_public_key[acct.address] = private_key

    return acct.address, private_key

def send_eth(sender_private_key, sender_addr, receiver_addr, gas_increase): #gas_increase
    #web3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e'))
    web3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e'))
    private_Key = sender_private_key
    from_address = sender_addr
    to_address = receiver_addr

    nonce = web3.eth.getTransactionCount(from_address)
    #gas = int('50')+gas_increase*10
    gasPrice = web3.toWei('50', 'gwei') #str(gas)
    value = web3.toWei(0.02, 'ether')

    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': value,
        'gas': 200000,
        'gasPrice': gasPrice
    }

    #sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_Key)

    #send transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    #Print transaction hash in hex
    print(web3.toHex(tx_hash))


# create 10 new accounts (use only once if dict_private_public_key is empty)
# dict_private_public_key = None #re-initialize if you want execute the code below
# for i in range(0,4):
#     newAccount()
# print(dict_private_public_key)

#send the transactions
#count = 0 #used to skip the first element in the dict, because it is the sender of transactions
# for i in dict_private_public_key:
#     time.sleep(20)
#     print("Gooo!")
#     if count >= 1:
#         send_eth("0xf641b77d995ebade72e5a96f065232d9057284581e6b3ef6cbc194896ce606fa","0x34c17b647dDd4E38CDC2F5B38efd1F42681cB889", i, count)
#     count += 1





#estimate the gas required by the smart contract
# address = "0x7402FD163860F2F561e9BB648B56ac2B5b9ED0E6"
# counter = Web3.eth.contract(address=address, abi=abi)