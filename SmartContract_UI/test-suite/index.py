from socket import timeout
from reach_rpc import mk_rpc
from threading import Thread
import random
import math
import json
import time
import sys
def main():
 
    rpc, rpc_callbacks = mk_rpc()


    print("The consensus network is: ", rpc("/stdlib/connector"));

    starting_balance = rpc("/stdlib/parseCurrency", 1000)

    acc_creator = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob1 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob2 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob3 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob4 = rpc("/stdlib/newTestAccount", starting_balance)

    acc_verifier1 = rpc("/stdlib/newTestAccount", starting_balance)
    
    
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

    before_creator = get_balance(acc_creator)
    before_bob1 = get_balance(acc_bob1)
    before_verifier1 = get_balance(acc_verifier1)

    SMART_CONTRAT_PAYMENT = ftm_eth(500000000000000000000)

    ctc_creator = rpc("/acc/contract", acc_creator)

    def player(who):
        def reportPosition(did,  proof_and_position):
            did_int = int(did.get('hex'), 16)
            print("DID inserted: ",did_int,"\tposition inserted: ",proof_and_position[1])

        def reportVerification(did, verifier):
            did_int = int(did.get('hex'), 16)
            print("DID ", did_int, " has been verified by Verifier ", verifier)
        return {'stdlib.hasConsoleLogger': True,
                'reportPosition': reportPosition,
                'reportVerification':reportVerification,
                }
    def play_Creator():
        # def reportPosition(did,  proof_and_position):
        #     print("report results, position inserted: ", proof_and_position[1])
        #     #print('New position inserted \n DID: %s did \n proof_and_position: %s proof_and_position' % str(did), proof_and_position[1])
        
        rpc_callbacks(
            '/backend/Creator',
            ctc_creator,
            dict(
                position="Bologna",
                decentralized_identifier=1,
                proof_reveived="PROOF",  
                #reportPosition= reportPosition,
                **player('Creator')
            ),
        )

    creator = Thread(target=play_Creator)
    creator.start()
    print("\t Creator started! Smart contract deployed. ")

    def play_bob(accc, pos, did):
        # Get and attach to the creator Contract
        ctc_bob = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_creator))
        # Call the API
        result_counter = rpc('/ctc/apis/attacherAPI/insert_position', ctc_bob, pos, did)
        counter_int = int(result_counter.get('hex'), 16)
        print("Number of users that can still insert their position: ", counter_int)
        rpc("/forget/ctc", ctc_bob)

    def verifier_pay(accc):
        ctc_verifier = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_creator))
        # Call the API
        money_payed = rpc('/ctc/apis/verifierAPI/insert_money', ctc_verifier, SMART_CONTRAT_PAYMENT)
        money_payed_int = int(money_payed.get('hex'), 16)
        print("money_payed by verifier to the contract ", money_payed_int/1000000000000000000)
        rpc("/forget/ctc", ctc_verifier)
        
    def verifier_api(accc, did_choose, wallet_toVerify):
        ctc_verifier = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_creator))
        # Call the API
        result_api = rpc('/ctc/apis/verifierAPI/verify', ctc_verifier, did_choose, wallet_toVerify)
        print("User with wallet address ", result_api, " has been verified!")
        rpc("/forget/ctc", ctc_verifier)
    
    print("\n\tProvers are inserting their position and, proof computed by witness, inside the smart contract")
    time.sleep(4)
    pos_bob = "Torino"
    did_bob = 2
    bob1 = Thread(target=play_bob(acc_bob1, pos_bob, did_bob))
    bob1.start()
    time.sleep(4)
    pos_bob = "Milano"
    did_bob = 3
    bob2 = Thread(target=play_bob(acc_bob2, pos_bob, did_bob))
    bob2.start()
    time.sleep(4)
    pos_bob = "Venezia"
    did_bob = 4
    bob3 = Thread(target=play_bob(acc_bob3, pos_bob, did_bob))
    bob3.start()
    time.sleep(4)
    # pos_bob = "San Lazzaro"
    # did_bob = 5
    # bob4 = Thread(target=play_bob(acc_bob4, pos_bob, did_bob))
    # bob4.start()

    time.sleep(4)
    #print("Verifier1 balance is: ", before_verifier1)
    print("\n\tVerifier1 is going to pay: ",  int(SMART_CONTRAT_PAYMENT.get('hex'),16)/1000000000000000000)
    verifier1 = Thread(target=verifier_pay(acc_verifier1))
    verifier1.start()
    verifier1_last = get_balance(acc_verifier1)
    
    print('Verifier1 went from %s to %s' % (before_verifier1, verifier1_last))
    ##### TODO: change the line below passing the address of the prover!!!!!!
    walletVerifier = format_address(acc_verifier1) # TODO: the wallet must be the PROVER wallet, now is the VERIFIER wallet

    did_choose = 1 #DID to verify

    print("\n\tVerifier1 is going to Verify someone")
    verifier1_verify = Thread(target=verifier_api(acc_verifier1, did_choose, walletVerifier))
    verifier1_verify.start()


    creator.join()
    bob1.join()
    bob2.join()
    bob3.join()
    #bob4.join()
    verifier1.join()
    verifier1_verify.join()

    after_creator = get_balance(acc_creator)
    print('Creator went from %s to %s' % (before_creator, after_creator))
    
    before_verifier1_last = get_balance(acc_verifier1)
    print("Verifier1 balance is now: ", before_verifier1_last) #TODO: print the balance of rewarded prover, not verifier!

    rpc('/forget/acc', acc_creator, acc_bob1, acc_bob2, acc_bob3, acc_bob4, acc_verifier1)
    rpc("/forget/ctc", ctc_creator)


if __name__ == '__main__':
    #startSimulation()
    main()
    
    sys.exit()









