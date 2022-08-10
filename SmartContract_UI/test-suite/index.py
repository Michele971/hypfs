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
    name = 'Alice'
    acc_alice = rpc("/stdlib/newTestAccount", starting_balance)
    acc_bob1 = rpc("/stdlib/newTestAccount", starting_balance)
    
    def fmt(x):
        return rpc("/stdlib/formatCurrency", x, 4)

    def get_balance(w):
        return fmt(rpc("/stdlib/balanceOf", w))

    before_alice = get_balance(acc_alice)
    before_bob1 = get_balance(acc_bob1)


    ctc_alice = rpc("/acc/contract", acc_alice)

    # def player(who):
    #     def reportPosition(did,  proof_and_position):
    #         print('New position inserted \n DID: %s did \n proof_and_position: %sproof_and_position' % did, proof_and_position)
        
    #     def report_results(results):
    #         print('Results %s' % results) 

    #     return {#'stdlib.hasConsoleLogger': True,
    #             'reportPosition': reportPosition,
    #             }
    def play_alice():
        def reportPosition(did,  proof_and_position):
            print("report results, position inserted: ", proof_and_position[1])
            #print('New position inserted \n DID: %s did \n proof_and_position: %s proof_and_position' % str(did), proof_and_position[1])
        
        rpc_callbacks(
            '/backend/Creator',
            ctc_alice,
            dict(
                position="Bologna",
                decentralized_identifier=1,
                proof_reveived="PROOF",
                reportPosition= reportPosition,#**player('Creator')
            ),
        )

    alice = Thread(target=play_alice)
    alice.start()
    print("\t Creator started!")

    def play_bob(accc):
        ctc_bob = rpc("/acc/contract", accc, rpc("/ctc/getInfo", ctc_alice))
        time.sleep(10)
        result_api = rpc('/ctc/apis/attacherAPI/insert_position', ctc_bob)
        print("result api ", result_api)
        rpc("/forget/ctc", ctc_bob)

    
    print("\t aaaaaa 0")
    time.sleep(4)
    bob1 = Thread(target=play_bob(acc_bob1))
    print("\t aaaaaa 1")
    bob1.start()
    alice.join()
    bob1.join()


    after_alice = get_balance(acc_alice)
    print('Alice went from %s to %s' % (before_alice, after_alice))
    
    rpc('/forget/acc', acc_alice, acc_bob1)
    rpc("/forget/ctc", ctc_alice)

if __name__ == '__main__':
    #startSimulation()
    main()










