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
SMART_CONTRAT_PAYMENT = rpc("/stdlib/parseCurrency", 500)

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
        lock.release()
        print("release the lock ")

    def reportVerification(did, verifier):
        did_int = int(did.get('hex'), 16)
        print("DID ", did_int, " has been verified by Verifier ", verifier)
    return {'stdlib.hasConsoleLogger': True,
            'reportPosition': reportPosition,
            'reportVerification':reportVerification,
            }

def play_Creator(contract_creator, position, did, proof):
    print("Lock is locked? ",lock.locked(),"\n",)
    lock.acquire()
    if lock.locked():
        print("\tlocked acquired")
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
    print("Lock is locked? ",lock.locked(),"\n",)
    lock.acquire()
    if lock.locked():
        print("\tlocked acquired")
    else:
        print("waiting for lock ...")
    # Get and attach to the creator Contract
    print("Entering in play_bob, attaching to: ", ctc_user_creator,'\n')    
    ctc_bob = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_user_creator))
    print("Attaching Done")
    # Call the API
    print("\nCalling the API ...")
    result_counter = rpc('/ctc/apis/attacherAPI/insert_position', ctc_bob, pos, did)
    #print("2) waiting 10 secs ... ")
    #time.sleep(10)
    counter_int = int(result_counter.get('hex'), 16)
    print("User ATTACHED  📎 📎 \n Number of users that can still insert their position: ", counter_int)
    print("\tReleasing lock ...")
    lock.release()
    print("Locked? ", lock.locked())
    print("\n\n")
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
        #print("User with wallet address ", result_api, " has been verified!")

        '''
            TODO: remove the address from "provers_addresses" list, if it is successfully verified!!!
        '''
        rpc("/forget/ctc", ctc_verifier)

def main():

    print("The consensus network is: ", rpc("/stdlib/connector"));

    starting_balance = rpc("/stdlib/parseCurrency", 1000) # use "parseCurrency" method when you send value TO backend

    acc_creator = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob1 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob2 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob3 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob4 = rpc("/stdlib/newTestAccount", starting_balance)


    acc_verifier1 = rpc("/stdlib/newTestAccount", starting_balance)
    
    before_creator = get_balance(acc_creator)
    before_bob1 = get_balance(acc_bob1)
    before_verifier1 = get_balance(acc_verifier1)

    ctc_creator = rpc("/acc/contract", acc_creator)


    position = "Bologna"
    did = '1'
    proof = 'proof_creator'

    #deploying the contract using the creator account
    creator = Thread(target=play_Creator, args=(ctc_creator, position, did, proof))
    creator.start()
    provers_addresses.append(format_address(acc_creator))
    print("\t Creator started! Smart contract deployed. ")
    
    def view_getCtcBalance(accc):
        ctc_bobs = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_creator))
        # call the view
        result_view = rpc("/ctc/views/views/getCtcBalance",ctc_bobs)
        print("Balance of the contract: ", ftm_eth(int(result_view[1].get('hex'), 16))) 
        rpc("/forget/ctc", ctc_bobs)
        
    def view_getReward(accc):
        ctc_users = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_creator))
        reward_amount = rpc("/ctc/views/views/getReward",ctc_users)
        print("Reward to pay ", int(reward_amount[1].get('hex'), 16))
        rpc("/forget/ctc", ctc_users)

    print("\n\tProvers are inserting their position and, proof computed by witness, inside the smart contract")
    time.sleep(4)
    pos_bob = "Torino"
    did_bob = 2
    bob1 = Thread(target=play_bob(ctc_creator, acc_bob1, pos_bob, did_bob, 'proof'))
    bob1.start()
    provers_addresses.append(format_address(acc_bob1))

    time.sleep(4)
    pos_bob = "Milano"
    did_bob = 3
    bob2 = Thread(target=play_bob(ctc_creator, acc_bob2, pos_bob, did_bob, 'proof'))
    bob2.start()
    provers_addresses.append(format_address(acc_bob2))

    time.sleep(4)
    pos_bob = "Venezia"
    did_bob = 4
    bob3 = Thread(target=play_bob(ctc_creator, acc_bob3, pos_bob, did_bob, 'proof'))
    bob3.start()
    provers_addresses.append(format_address(acc_bob3))

    # time.sleep(4)
    # pos_bob = "San Lazzaro"
    # did_bob = 5
    # bob4 = Thread(target=play_bob(ctc_creator, acc_bob4, pos_bob, did_bob, 'proof'))
    # bob4.start()
    # provers_addresses.append(format_address(acc_bob4))


    time.sleep(4)
    #print("Verifier1 balance is: ", before_verifier1)
    print("\n\tVerifier1 is going to pay: ", SMART_CONTRAT_PAYMENT)
    verifier1 = Thread(target=verifier_pay(ctc_creator, acc_verifier1))
    verifier1.start()
    verifier1_last = get_balance(acc_verifier1)
    
    print('Verifier1 went from %s to %s' % (before_verifier1, verifier1_last))

    ######## some tests
    # someone verify the contract balance
    bobViewGetBalance = Thread(target=view_getCtcBalance(acc_bob1))
    bobViewGetBalance.start()

    userView_getReward = Thread(target=view_getReward(acc_bob1))
    userView_getReward.start()
    ######## end tests

    ##### TODO: change the line below passing the address of the prover!!!!!!
    walletVerifier = format_address(acc_verifier1) # TODO: the wallet must be the PROVER wallet, now is the VERIFIER wallet

    did_choose = 2 #DID to verify

    print("\n\tVerifier1 is going to Verify someone")
    verifier1_verify = Thread(target=verifier_api_verify(ctc_creator, acc_verifier1, did_choose, provers_addresses[1])) # in this case, the verifier is going to verify the bob1
    verifier1_verify.start()

    #################### start some testing steps ####################
    creator_last = get_balance(acc_creator)
    print("CREATOR balance is now: ", creator_last) #TODO: print the balance of rewarded prover, not verifier!
    print("WALLET CREATOR: ", provers_addresses[0])

    after_bob1 = get_balance(acc_bob1)
    print("accBob1 balance is now: ", after_bob1)
    print("WALLET BOB: ", provers_addresses[1])

    print("WALLET VERIFIER: ", walletVerifier)
    #################### end some testing steps ####################

    creator.join()
    bob1.join()
    bob2.join()
    bob3.join()
    #bob4.join()
    verifier1.join()
    bobViewGetBalance.join()
    userView_getReward.join()
    verifier1_verify.join()

    after_creator = get_balance(acc_creator)
    print('Creator went from %s to %s' % (before_creator, after_creator))
    
    rpc('/forget/acc', acc_creator, acc_bob1, acc_bob2, acc_bob3, acc_bob4, acc_verifier1) 
    rpc("/forget/ctc", ctc_creator)


if __name__ == '__main__':
    main()
    
    sys.exit()









