from hashlib import new
from eth_account import Account
import secrets
from web3 import Web3
import time
# public key is the key - private key is the value
dict_private_public_key = {
    '0x832e977393410e0388f994bb773d78E83Ae9619E': '0x8d10e8fb1aa289828f31914f581dbc39d9ed76b2e2d1247c49f5814349ff10c0',
    '0x119d2BA2e52e21A88210Cd29DA0c7d45D2AC077A': '0x9cf648f6aaa283e0c227f9047e735e1d604875ce735223c334f1c511a0dd2b1b',
    '0xf373B8b4BcDEbD88efC8396b5420A41fE7c94011': '0xd1d2862447f71d78ab4d0b92800034c11cb7bd13ffe5d0a5bc2851e95ce719d7',
    '0x1eAd4c7aa92bABF7c923a8E597972CB3255Ab6C2': '0x0fcab881cf4b6d40fbf1473b908d9501524b0d84ac7fe44196e763b8bde9545a',
    '0xe648143d83F7dD8eaaD587B9DDE0E40b7eFE0d62': '0x18c78ad1e9447f077611e1945579c4215bb5551852e8b4957c89b783eb1aa3c8',
    '0x7211170e1CF574642857f98f7afA14990C39c75c': '0x3c5baad76449c59aa1cff6d27febaa201d5150b86b382451d3645d8afd919a63',
    '0xC57D9AD7164af80AC324081D2A206179F567fECE': '0xc662ab78a9180104c1d20f9eb1f993794c093e98e7efe78e23d5ccb02fec637f',#
    '0xBAa6cD46581b66E379c3B5436fa678976B34A518': '0xbd0c0a94a5998144da5a64c5ca9c67cc92d383762fa58b7e8017eed63de908b4',
    # '0x6dd3FdD9752c5f935F1bF88542ab26D65eAC2B40': '0x8ad4d716b3ed5c31cf4125fed2f9549259768482941f7ea3969d0fda93413e06',
    # '0x4c992e7D1fBfBa8Cd4cc429C5d1105ACbd9BAC45': '0x3888a91f2bae15a5c8df4545ecc2b2a50ea2f0034ec168df7ae429987eabf405'
}

def newAccount():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    print("Address:", acct.address)
    print ("Private key:", private_key)
    #dict_private_public_key[acct.address] = private_key

    return acct.address, private_key

def send_eth(sender_private_key, sender_addr, receiver_addr): #gas_increase
    web3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e'))
    private_Key = sender_private_key
    from_address = sender_addr
    to_address = receiver_addr

    nonce = web3.eth.getTransactionCount(from_address)
    #gas = int('50')+gas_increase*10
    gasPrice = web3.toWei('50', 'gwei') #str(gas)
    value = web3.toWei(0.4, 'ether')

    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': value,
        'gas': 2000000,
        'gasPrice': gasPrice
    }

    #sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_Key)

    #send transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    #Print transaction hash in hex
    print(web3.toHex(tx_hash))

newAccount()

# create 10 new accounts (use only once if dict_private_public_key is empty)
# dict_private_public_key = None #re-initialize if you want execute the code below
#for i in range(0,10):
    #newAccount()
# print(dict_private_public_key)

#send the transactions
# count = 0 #used to skip the first element in the dict, because it is the sender of transactions
# for i in dict_private_public_key:
#     time.sleep(20)
#     print("Gooo!")
#     if count >= 1:
#         send_eth("0x8d10e8fb1aa289828f31914f581dbc39d9ed76b2e2d1247c49f5814349ff10c0","0x832e977393410e0388f994bb773d78E83Ae9619E", i, count)
#     count += 1

#send_eth("0x8d10e8fb1aa289828f31914f581dbc39d9ed76b2e2d1247c49f5814349ff10c0","0x832e977393410e0388f994bb773d78E83Ae9619E", "0x4c992e7D1fBfBa8Cd4cc429C5d1105ACbd9BAC45")
