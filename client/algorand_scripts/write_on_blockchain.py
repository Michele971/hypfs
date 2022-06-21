from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
#from src.utils import *
PURE_STAKE_API_KEY = "nYYIqswHmq3C0xpWSNUYb8073dFpTUAu6tg1GXlw"


mnemonic_secret = "desert laundry solution prosper miss inform above control loan ketchup forget farm tourist author gain shove sure film solar brain physical vocal quote ability volume"
account_a_private_key = mnemonic.to_private_key(mnemonic_secret)
account_a = mnemonic.to_public_key(mnemonic_secret)
#account_b = '4MA2FVCWUGDVAN3RD2E2JHBPAHR7USXLPADGQLWM2YBZYECGDJ2UCC2JGA'
account_b = '7YEPQKFVKJKFQJJVU5XMS22RZL3NSB2WLYZQO5HMWABUNF4MBFSRIMDB5Q'


purestake_key = "nYYIqswHmq3C0xpWSNUYb8073dFpTUAu6tg1GXlw"
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
    print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txinfo

def make_transaction():
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    last_valid_round = params.last
    tx_fee = params.min_fee
    tx_amount = 0
    note = '{"firstName":"AAAAA", "LastName":"AAAAAAAAAA"}'.encode()

    # Create and sign transaction
    tx = transaction.PaymentTxn(account_a, tx_fee, first_valid_round, last_valid_round, gen_hash, account_b, tx_amount, None, note)
    signed_tx = tx.sign(account_a_private_key)

    try:
        # Send the transaction
        # note that the PureStake api requires the content type for the following call to be set to application/x-binary
        tx_confirm = acl.send_transaction(signed_tx)
        print('Transaction sent with ID', signed_tx.transaction.get_txid())
        wait_for_confirmation(acl, txid=signed_tx.transaction.get_txid())

        print("Done.")
        print("Sent " + str(tx_amount) + " microalgo in transaction: " + str(tx_confirm))
        print("")

        # Query resulting balances
        result = acl.account_info(account_a)
        print(result["address"] + ": " + str(result["amount"]) + " microalgo")


    except Exception as e:
        print(e)


