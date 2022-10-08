from hashlib import new
from eth_account import Account
import secrets
from web3 import Web3
import time

#This script has been used to create new Ethereum accounts and send them some money.


# public key is the key - private key is the value
dict_private_public_key = {
    '0x34c17b647dDd4E38CDC2F5B38efd1F42681cB889': '0xf641b77d995ebade72e5a96f065232d9057284581e6b3ef6cbc194896ce606fa',
    #'0xAc18Ec4c7f390663B179a7891f26247612654c8c': '0x833170377ef9e0cac6ae75989fed851279b723d12cfa880023adff5f341c8ab0',  
    #'0xF8f1AAcEDf0dBB07693f76e807e4EF9a96A6Aa9f': '0x9de62bf46a345f949b6e2f07088a626f07e84f7ca4269917188573a0b1d0be4b', 
    # '0x91EF6D0F7c12b5FF0c1F81DCFFAF1e30BF0F52D7': '0xc291f9aea360cc6d09a5bc071af3ee5e29a18bee02f4d39ed9f50633c7863eb1',

    # '0x5381113B7b13c15af3a534065001EdeB2476802c':'0xb8b60ef412eeb95643e5701ec56b5fb11698d576e08127c33f893949386a5e45',
    #'0xA6Abd9eB42aad1b98c2a9dF0B4E2E3c743162ba5':'0xafe6f14b10d9a6693f04ebc1bf2090b406a89ffdb97713c9bf122e961b46c39d',
    #'0x87985fC3dCE979C09E3c3e745A7A0B464540CA82':'0x50e50c32c43bc3b55ed7cdffacc03780508fe20774f8255989ab971415271cf4',
    # '0x1fE37BD94109bA874a235B44fA79fC2d7710F1B0':'0x8778e9ea55646607d276cc9ac858097e4b9ad3bb171b1d0a96d98b32f298c760',

    # '0xfbe72863099f8fCAFe6Df5626692013Ce2e83ec3':'0x9e5cd974573308612579e29c2f1ba9899c5622cd273bcc00941acdb107260199', 
    # '0x7e90fCc0B6a4459A2c47A2b015c37fB5340aCcb5':'0x12f576f887df544a76fbd88a79dafc852b9900e328b2a448450bc5fe4b60589a', 
    # '0xC4A9067cE5542899510e6cB8A2Eb84A0a0953eDE':'0xf285e21ad35d451453a0e11f1c2580316a66b74126528303f52d93dfa9d1dee3', 
    # '0x63d3e6E0d2E762570819086f3E6dEF5061a27890':'0x31c2d8d88b2de858e6a76f35b410bf68f24d9033a6d549111e12a91974895f3e', 

    # '0x7b3180CFeBc06f78Cc55D2bA19cA24dfa2d1fe44':'0x1cb11272fb93f95c3e1e1be4158732133350eba49df1e5fe13adb06a572066dd', 
    # '0x9F81B843da3c2d66b08d7Af60c1FE7D79e20771E':'0xd35e2d01b9a22f00a84af71642aecf79ea9c7c84cbcba9171ba96a2555245ad7', 
    # '0xf71Fea9ED70597c365B5D8A2bD78e04E31654c5e':'0x1aea64ed14d59cc0daf0f0a9df7f00ff0f5382bb548ca1b12e293b3e4ed6c638', 
    # '0x1aF193411dDf746C501459406e8f00f465E11433':'0xa8f490477bdff610b4bc6ed10c6859e370c5d56c747253f7bfa8253b64b26840',

    # '0x3AC3A765E4669E0e124C8f1E5104F56a051F7F62':'0x46fca04375b753148d711abd1f00e370d9a4da8d612b2d0e9f8799290028df90', 
    # '0x605Ef12afC9912fE95A8B9b75b5e9E777AEb7107':'0x6f2467cf0dc2b02757ca25ab0c9e112971637e45249075fc78074c0a5cff6206', 
    # '0xe61B884f7E7DEa7413c6d65889bC04632241f81d':'0xbf39de3dfca255ecc39d786d1e74eb0ac7995db651258f061d1dbb56f7c62b1d', 
    # '0xee366FBffcFE70B50BbFD6ba3eD9563743ED33cb':'0xc5b48a5c9e0353f7f2a5cc249b6ffb704c2c4975e25b0a21b2a20f8f23619945',

    '0xA6657AE3cd2444d523408B3453cB4014eE6eA461':'0x16e2f555ace3ac16266a406ce44484578a4a856cc94a9122828fb002e3588672', 
    '0xf3feFd5613A47684A91246e5a9Fb5945983a86c0':'0xb4180e90b27d9b6f0b49b7213f11dfaaa575b03ada1e68de0a4f3017f93cfc87', 
    '0xF13D193A1f808AF9a132C75D40B3934abdeA037e':'0x4237e0ad41e03dd26c40a6e9a3856161ef040cef4fc68beea788a8c4bbfd5b56', 
    '0x3d424297c1375222C4EafFF32a9aF8bD87eF1C34':'0x8ed2c32dffbd3fee83ae8dddef2e2cb33de835a6e891f3ff1d5a6a3a8c593c49'
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
    #web3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e'))

    private_Key = sender_private_key
    from_address = sender_addr
    to_address = receiver_addr

    nonce = web3.eth.getTransactionCount(from_address)
    '''
        Since I can have more than one pending transaction, they could have same nonce and similar gas fee. 
        I have to increment the gas fee in order to avoid 'repleacement transaction underpriced' error.
    '''
    gas = int('50')+gas_increase*10
    gasPrice = web3.toWei(str(gas), 'gwei') #str(gas)
    value = web3.toWei(0.4, 'ether')

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
# for i in range(0,8):
#     newAccount()
# print(dict_private_public_key)

#send the transactions
#count = 0 #used to skip the first element in the dict, because it is the sender of transactions
# for i in dict_private_public_key:
#     if count >= 1:
#         time.sleep(20)
#         print('Send to: ',i)
#         send_eth("0xf641b77d995ebade72e5a96f065232d9057284581e6b3ef6cbc194896ce606fa","0x34c17b647dDd4E38CDC2F5B38efd1F42681cB889", i, count)
#     count += 1





#estimate the gas required by the smart contract
# address = "0x7402FD163860F2F561e9BB648B56ac2B5b9ED0E6"
# counter = Web3.eth.contract(address=address, abi=abi)