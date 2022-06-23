from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from src.utils import *


mnemonic_secret = "desert laundry solution prosper miss inform above control loan ketchup forget farm tourist author gain shove sure film solar brain physical vocal quote ability volume"


purestake_key = PURE_STAKE_API_KEY
endpoint_address = 'https://testnet-algorand.api.purestake.io/ps2'
header = {
    "X-API-Key": purestake_key,
    }
acl = algod.AlgodClient(purestake_key, endpoint_address, header)

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print('Waiting for confirmation')
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    #print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txid, txinfo

def make_transaction(algorand_wallet_passphase,obj_hash):
    '''
        With this function we store the hash of the IPFS object and store it inside a 
        transaction of Algorand Blockchain.
        In particular, we insert the hash inside the note field.

        Sequently, the id of transaction will be stored inside the DHT.

        The original project, without Algorand, stored hash of IPFS in the DHT not the transaction ID. 
    '''
    account_a_private_key = mnemonic.to_private_key(algorand_wallet_passphase)
    algorand_wallet_address = mnemonic.to_public_key(algorand_wallet_passphase)
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    last_valid_round = params.last
    tx_fee = params.min_fee
    tx_amount = 0

    note0 = '{"ipfs_obj_hash":"'+obj_hash+'"}'
    note = note0.encode() 

    # -----------> TODO: Send the transaction to a specific address: the address of the COMPANY 
    # Create and sign transaction. The transaction is sent to itself (the same address). 
    tx = transaction.PaymentTxn(algorand_wallet_address, tx_fee, first_valid_round, last_valid_round, gen_hash, algorand_wallet_address, tx_amount, None, note)
    signed_tx = tx.sign(account_a_private_key)


    try:
        # Send the transaction
        # note that the PureStake api requires the content type for the following call to be set to application/x-binary
        tx_confirm = acl.send_transaction(signed_tx)
        txid_confirmed = wait_for_confirmation(acl, txid=signed_tx.transaction.get_txid())
        print("Done.")
        # Query resulting balances
        result = acl.account_info(algorand_wallet_address)

        #return the transaction ID
        return txid_confirmed[0]
        

    except Exception as e:
        print(e)


