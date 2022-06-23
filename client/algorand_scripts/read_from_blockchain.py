from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from src.utils import *
import json
import base64



# using PureStake API
def read_transaction(tx_id):
    purestake_key = PURE_STAKE_API_KEY
    url = "https://testnet-algorand.api.purestake.io/idx2/v2/transactions/"+tx_id    
    headers = {
        "x-api-key": PURE_STAKE_API_KEY,
    }


    response = requests.get(url,headers=headers)
    #print("ponyyyyyy ",response.json()['transaction']['note'])
    data = response.json()["transaction"]["note"]
    person_dict = json.loads(base64.b64decode(data).decode())

    print("hash IPFS trovato = {}".format(person_dict['ipfs_obj_hash']))
    return person_dict['ipfs_obj_hash']