from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from src.utils import *
from menu import input_string

mnemonic_secret = "desert laundry solution prosper miss inform above control loan ketchup forget farm tourist author gain shove sure film solar brain physical vocal quote ability volume"
account_a_private_key = mnemonic.to_private_key(mnemonic_secret)
account_a = mnemonic.to_public_key(mnemonic_secret)
account_b = mnemonic.to_public_key(mnemonic_secret) #the transaction is sent to the same account: 4MA2FVCWUGDVAN3RD2E2JHBPAHR7USXLPADGQLWM2YBZYECGDJ2UCC2JGA


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
        #print('Waiting for confirmation')
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    #print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txinfo

def make_transaction(algorand_wallet_passphase):
    account_a_private_key = mnemonic.to_private_key(algorand_wallet_passphase)
    algorand_wallet_address = mnemonic.to_public_key(algorand_wallet_passphase)
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    last_valid_round = params.last
    tx_fee = params.min_fee
    tx_amount = 0
    note = '{"firstName":"Lerry", "LastName":"Pony"}'.encode()

    # Create and sign transaction
    tx = transaction.PaymentTxn(algorand_wallet_address, tx_fee, first_valid_round, last_valid_round, gen_hash, account_b, tx_amount, None, note)
    signed_tx = tx.sign(account_a_private_key)

    try:
        # Send the transaction
        # note that the PureStake api requires the content type for the following call to be set to application/x-binary
        tx_confirm = acl.send_transaction(signed_tx)
        #print('Transaction sent with ID', signed_tx.transaction.get_txid())
        wait_for_confirmation(acl, txid=signed_tx.transaction.get_txid())

        #print("Done.")
        #print("Sent " + str(tx_amount) + " microalgo in transaction: " + str(tx_confirm))
        #print("")

        # Query resulting balances
        result = acl.account_info(algorand_wallet_address)
        #print(result["address"] + ": " + str(result["amount"]) + " microalgo")


    except Exception as e:
        print(e)


