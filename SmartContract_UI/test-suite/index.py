from socket import timeout
from reach_rpc import mk_rpc
from threading import Thread, Lock
import random
import math
import json
import time
import sys
from datetime import datetime

lock = Lock()

provers_addresses = [] # this address need to be verified
start_list = [] #start time
end_list = [] #end time

rpc, rpc_callbacks = mk_rpc()
SMART_CONTRAT_PAYMENT = rpc("/stdlib/parseCurrency", 0.5)

def fmt(x):
    return rpc("/stdlib/formatCurrency", x, 4)

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
        print("The lock is locked? ", lock.locked())
        if lock.locked():
            lock.release() # This is the only the momente when someone release the lock
            print("release the lock AFTER INSERTING INFORMATION ")
            end_list.append(time.time())


    def reportVerification(did, verifier):
        did_int = int(did.get('hex'), 16)
        print("DID ", did_int, " has been verified by Verifier ", verifier)
    return {'stdlib.hasConsoleLogger': True,
            'reportPosition': reportPosition,
            'reportVerification':reportVerification,
            }

def play_Creator(contract_creator, position, did, proof):
    print("CREATOR Lock is locked? ",lock.locked(),"\n",)
    lock.acquire()
    if lock.locked():
        print("\tCREATOR: locked acquired")
    else:
        print("waiting for lock ...")
        
    start_list.append(time.time())
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
  
    start_list.append(time.time())

    # Get and attach to the creator Contract
    #print("Entering in play_bob, attaching to: ", ctc_user_creator,'\n')    
    ctc_bob = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_user_creator))
    # Call the API
    result_counter = rpc('/ctc/apis/attacherAPI/insert_position', ctc_bob, pos, did)

    counter_int = int(result_counter.get('hex'), 16)
    print("ATTACHER  📎 📎 \n Number of users that can still insert their position: ", counter_int," contract: ",ctc_user_creator )

    rpc("/forget/ctc", ctc_bob)









