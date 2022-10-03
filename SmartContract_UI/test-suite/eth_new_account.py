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
    '0xC57D9AD7164af80AC324081D2A206179F567fECE': '0xc662ab78a9180104c1d20f9eb1f993794c093e98e7efe78e23d5ccb02fec637f',
    '0xBAa6cD46581b66E379c3B5436fa678976B34A518': '0xbd0c0a94a5998144da5a64c5ca9c67cc92d383762fa58b7e8017eed63de908b4',
    '0x6dd3FdD9752c5f935F1bF88542ab26D65eAC2B40': '0x8ad4d716b3ed5c31cf4125fed2f9549259768482941f7ea3969d0fda93413e06',
    '0x4c992e7D1fBfBa8Cd4cc429C5d1105ACbd9BAC45': '0x3888a91f2bae15a5c8df4545ecc2b2a50ea2f0034ec168df7ae429987eabf405',
    '0x5a2a37163523509Dee3B48D6740E5F25A8654Cb6': '0xf5568735c8cb26c544944dc1e6025dd94c9a9d7f7422ea8168f417167d513867',
    '0x5DE99700870d455DF99B3afCa0e7Cd85e8fF2f3d': '0x512981281c472444fa4d8b73866cc2b1235424bec8129eb448661c36134ff8ac',

    '0x0E6ccE4c7C1AA5057c01c9c776168dC412d593f4': '0x8daea43f6969c5af179e890a2b05d7bbe4e65f33eaae2b1bacc12e70da03ab3e',
    '0x199986ccBe425ef98a53C373A579b0d64F5daD3D': '0x58db0a6d84722ba10fb1b6f57c127b9858c4d5be2c15ff9d15d6c9173dcaca86',
    '0xA7953c30BD1Ae955ed19C162B0AEc2483c51c73D': '0xa8597bc7404aa73371e6631e4471eb9d10204a5622fe3441a657bd226a296c8b',
    '0x16C09e450A17B6De918D6637343700d7C6dB5d0d': '0xafea88fd0911cbd04c2755d02792951da04bd542e0243e6e6cba2d2a0becb804'
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
    value = web3.toWei(1, 'ether')

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

newA, priv = newAccount()
send_eth("0x8d10e8fb1aa289828f31914f581dbc39d9ed76b2e2d1247c49f5814349ff10c0", "0x832e977393410e0388f994bb773d78E83Ae9619E", newA)

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
