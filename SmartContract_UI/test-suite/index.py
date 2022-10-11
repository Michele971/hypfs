from socket import timeout
from reach_rpc import mk_rpc
from threading import Thread, Lock
import random
import math
import json
import time
import sys

lock = Lock()

provers_addresses = [] # this address need to be verified
rpc, rpc_callbacks = mk_rpc()
SMART_CONTRAT_PAYMENT = rpc("/stdlib/parseCurrency", 4/100) # the Smart contract will contain: 0.04 ETH (the reward will be 0.001)

def fmt(x):
    return rpc("/stdlib/formatCurrency", x, 4)

'''
    Because there are 1,000,000,000,000,000,000 WEI in 1 ETH, "BigNumber" is used to represet values in WEI ( 1000000000000000000).
    Quantities of a network token should always be passed into Reach in the token's atomic unit.    
    In particular, if the value comes FROM backend you will have to format it with "ftm_eth()" function. 
'''
def ftm_eth(x):
    return rpc("/stdlib/bigNumberify",x)

def get_balance(w):
    return fmt(rpc("/stdlib/balanceOf", w))

#this function take an account as input and prepare it for the backend
def format_address(account):
    addr = rpc("/acc/getAddress", account) # get the address associated to a specific account. Transactions can be send to this address (inside backend)
    return addr

def player(who):
    def reportPosition(did,  proof_and_position):
        did_int = int(did.get('hex'), 16)
        print("📝 DID inserted: ",did_int,"\tposition inserted: ",proof_and_position[1])
        # not always is locked, only when creator call the lock. The attacher NEVER call the lock!!!
        if lock.locked():
            lock.release() # This is the only the momente when someone release the lock
            print("release the lock AFTER INSERTING INFORMATION ")

    def reportVerification(did, verifier):
        did_int = int(did.get('hex'), 16)
        print("DID ", did_int, " has been verified by Verifier ", verifier)

    def issueDuringVerification(did):
        print("DID ",did, "has NOT been verified. Maybe there is an error inside the smart contract backend\t Maybe the contract balance is insufficient for execute the transfer")
        
    return {'stdlib.hasConsoleLogger': True,
            'reportPosition': reportPosition,
            'reportVerification':reportVerification,
            'issueDuringVerification':issueDuringVerification,
            }

def play_Creator(contract_creator, position, did, proof):
    print("CREATOR Lock is locked? ",lock.locked(),"\n",)
    lock.acquire()
    if lock.locked():
        print("\tCREATOR: locked acquired")
        print("Smart contract deployed  🚀 :", contract_creator)

    else:
        print("waiting for lock ...")
        
    rpc_callbacks(
        '/backend/Creator',
        contract_creator,
        dict(
            position=position,
            decentralized_identifier=did,
            proof_reveived=proof,  
            **player('Creator')
        ),
    )
  


def play_bob(ctc_user_creator, accc, pos, did, proof):
    print("ATTACHER Lock is locked? ",lock.locked(),"\n",)
    lock.acquire()

    ctc_bob = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_user_creator))
    # Call the API
    result_counter = rpc('/ctc/apis/attacherAPI/insert_position', ctc_bob, pos, did)
    counter_int = int(result_counter.get('hex'), 16)
    print("ATTACHER  📎 📎 \n Number of users that can still insert their position: ", counter_int," contract: ",ctc_user_creator )

    rpc("/forget/ctc", ctc_bob)



def verifier_pay(ctc_user_creator,accc):
        ctc_verifier = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_user_creator))
        # Call the API
        money_payed = rpc('/ctc/apis/verifierAPI/insert_money', ctc_verifier, SMART_CONTRAT_PAYMENT)
        #money_payed_int = int(money_payed.get('hex'), 16)
        #print("money_payed by verifier to the contract ", ftm_eth(money_payed_int))
        rpc("/forget/ctc", ctc_verifier)

def verifier_api_verify(ctc_user_creator, accc, did_choose, wallet_toVerify):
        ctc_verifier = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_user_creator))
        # Call the API
        result_api = rpc('/ctc/apis/verifierAPI/verify', ctc_verifier, did_choose, wallet_toVerify)
        rpc("/forget/ctc", ctc_verifier)
