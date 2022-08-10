from socket import timeout
from reach_rpc import mk_rpc
from threading import Thread
import random
import math
import json
import time

def main():
    rpc, rpc_callbacks = mk_rpc()


    print("The consensus network is: ", rpc("/stdlib/connector"));

    starting_balance = rpc("/stdlib/parseCurrency", 100)

    acc_alice = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob1 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob2 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob3 = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob4 = rpc("/stdlib/newTestAccount", starting_balance)

    acc_verifier1 = rpc("/stdlib/newTestAccount", starting_balance)
    
    
    def fmt(x):
        return rpc("/stdlib/formatCurrency", x, 4)

    def get_balance(w):
        return fmt(rpc("/stdlib/balanceOf", w))

    before_alice = get_balance(acc_alice)
    before_bob1 = get_balance(acc_bob1)


    ctc_alice = rpc("/acc/contract", acc_alice)

    def player(who):
        def reportPosition(did,  proof_and_position):
            print("DID inserted: ",did)
            print("position inserted: ",proof_and_position[1])

        return {'stdlib.hasConsoleLogger': True,
                'reportPosition': reportPosition,
                }
    def play_alice():
        # def reportPosition(did,  proof_and_position):
        #     print("report results, position inserted: ", proof_and_position[1])
        #     #print('New position inserted \n DID: %s did \n proof_and_position: %s proof_and_position' % str(did), proof_and_position[1])
        
        rpc_callbacks(
            '/backend/Creator',
            ctc_alice,
            dict(
                position="Bologna",
                decentralized_identifier=1,
                proof_reveived="PROOF",  
                #reportPosition= reportPosition,
                **player('Creator')
            ),
        )

    alice = Thread(target=play_alice)
    alice.start()
    print("\t Creator started!")

    def play_bob(accc, pos, did):
        ctc_bob = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_alice))

        result_api = rpc('/ctc/apis/attacherAPI/insert_position', ctc_bob, pos, did)
        print("result api ", result_api)
        rpc("/forget/ctc", ctc_bob)

    def play_verifier(accc):
        ctc_verifier = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_alice))

        result_api = rpc('/ctc/apis/verifierAPI/insert_money', ctc_verifier, fmt(5))
        print("result api ", result_api)
        rpc("/forget/ctc", ctc_verifier)
    

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

    
    verifier1 = Thread(target=play_verifier(acc_verifier1))
    verifier1.start()

    alice.join()
    bob1.join()
    bob2.join()
    bob3.join()
    #bob4.join()
    verifier1.join()

    after_alice = get_balance(acc_alice)
    print('Alice went from %s to %s' % (before_alice, after_alice))
    
    rpc('/forget/acc', acc_alice, acc_bob1, acc_bob2, acc_bob3, acc_bob4, acc_verifier1)
    rpc("/forget/ctc", ctc_alice)

if __name__ == '__main__':
    #startSimulation()
    main()










