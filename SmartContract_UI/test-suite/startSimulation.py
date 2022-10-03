
from platform import python_branch
from openlocationcode import openlocationcode as olc
from reach_rpc import mk_rpc
from index import format_address
from index import play_Creator, play_bob
from threading import Thread
import time
from index import start_list, end_list # list that contain start and end time for each thread
import numpy as np
import matplotlib.pyplot as plt
from makeTransaction import *
import concurrent.futures
'''
    ---------------------------------------------------------------------------------------
    ------------------    THIS SCRIPT MUST BE RUN ON ALGORAND TESTNET    ------------------
    ---------------------------------------------------------------------------------------
'''

list_private_public_key = [
    'enact spoon inquiry wolf wait process weather earn raven glare winner enter tell mandate cement harbor garment problem crowd banner replace lounge sight abstract topple', # GIM3KUP5473BIGGJZ3GNDREHC2YT2P4W4WJZXDILWLAYI57A4GAML33DRY
    'honey city during awkward flush destroy decrease hero rhythm fog insect year miss ship mention wage fan crop angle harsh demise banner addict absent what', #O47RCDX6L725MCPKEQNWWCMZAMR3UNIUYSKKV7N5UEAZDC2A6HPPID4C7Q
    'seed record photo dress unique that uniform urban bone ritual drive nose wolf miracle neither old gentle trend stage crisp rate fitness legal ability empty', #C5PCYMHJJPL5HBVL7KOJ5EXXNYOZCWYRKEP5NMNC6Z44CQLWABDDSZFBKI
    'describe reunion balcony empower pool work gown armed supreme negative garage minute crucial endless robust divide accuse resemble lava announce share quarter dentist abstract sight', #7EH36BDEHMHFYJUISRA4QZYIHCCN5U4ZEQ3Q64T7OAYSMIRARZ3Q6C6F3E
    'stool west normal magic option valve enrich vibrant knee total always shrug volcano fury ignore law second portion few uncover disease wreck green absorb bag', #5RW4HL5YY6FMYSICN5LYCCWM4LRXGNGJPU3RYW3SVRKADB7N2Z7OOIKZ7E
    'nose shell amount fossil manual letter shove cage damage fault initial insect border assume draft dawn number market giant movie parrot gentle police able hospital', #X56EISCBSSPAS75S2RZFJVBEXMGCVI2WG4QMIHRRCAHUGTCUGF7RE6643M
    'stable actress ordinary coral end potato approve coyote swap armed color clock eyebrow reject section thank host sense agree put sure replace area absorb echo', #2PDAQC47IFBJNU5AETJA2OV3I6NKDF4AAIZRG72ALDXMAUCEOO4KZPOO4E
    'people menu yellow vote twist guitar bargain will horse mammal usual hammer enroll input liar flower noise shy window ill clinic grape bar abstract estate', #BDFYNQR2I3YQR6WMTBYRYDJXCXDLIW5T22DVKT4IVL6R4ZQVI336E3VDNQ
    'lift decade sausage turtle pipe cup piece caution educate carpet provide barrel asset library topic hood flip swallow hotel assist dignity winner chimney absorb cost', #3YMI5U6ZKH3MZ3DNYWO3YL3SCH75KBBCWO2XOO2HEVFQSX3G2Y4UYPOWWA
    'divorce ecology panel wash curious rich chunk spy piece position hip great random fashion rice visual obey powder borrow chief fade sibling art able borrow', #7TIHVKNIGJF5H37SJDWWKOOT4FRUE4XDUGCZ77HZVKAEAHAWKLSS2LXRUQ
    
    'steak gauge carpet assume swamp tuna orphan athlete script inhale garment quiz critic exotic among turn obscure kitten modify width jacket tilt miss ability fence', # HKCHIEF5XKK6NYAYUBWHTX3JB7H62QQ36RWPUPNBGL75SXQB27ZWX5Q6DQ
    'chaos average someone regular luggage arena era parrot reason imitate yellow buyer clean enrich library pulse buddy shaft flip finger flip network theme abandon proof', # 22X4O3I5FSGYK4XTMWL6OEPKX7FPBI3QH4BB42VIZ75J7GVUDJZYCJ56OA
    'escape leg warm silver biology silk swallow wet ticket decrease seat speed drift nice give clerk find gather verb cube assume around gather abandon month', # QF25BWUJIY3NDFS47EILAOV4DAAHIYC2PRVIGERSQVTJ7RXHY44QBA6KO4
    'decline auction milk please lens quiz eight rough affair possible forum brand sing bless comfort believe exist twenty invest apart mask gesture match abstract marine', # MJXSIP7ULI25QH3XJP7AVQT7ZYO3TARYVUYRD6ARR6L6HWGH22ECU5MHAE
    'whisper giggle spot sadness loyal menu cliff sense flash share guide exit oak loud field inch during slender clump loyal stove enter album abstract wool', # XSKXAH4SIWFOLFUWS6H73JUJ5HJOWUCBKTA6LFXFCYS6VDZMQL6RI5HGQM
    'wide theme range pulse husband clever cruel kid double right choice match ill bless garlic flash zoo around ability creek exist armed hand able service' # JI7VRGDIANFNABPJL6PWVGCP42NZGQVV7T3QVJD6P47EKQP2BXSFMPU7RA
]

prover_thread = [] #list of prover thread
prover_list_account = [] #list of prover account 
prover_addresses = [] # list of provers addresses

contract_creator_deployed = None # contrat deployed, will have to be a list of contracts

rpc, rpc_callbacks = mk_rpc()
rpc("/stdlib/setProviderByName","TestNet")

print("\t\t The consesus network is: ", rpc('/stdlib/connector'))
STARTING_BALANCE = rpc("/stdlib/parseCurrency", 1500) 
location_in_hypercube = False # simulate if the location is already stored in hypercube


PROVER_NUMBER = 4 # number of provers for the entire system

'''
    ❗️❗️❗️❗️  WARNING: ❗️❗️❗️❗️
    ---> len(DID_LIST_PROV) and len(LOCATION_LIST_PROV) MUST TO BE EQUALS !!! You can decrease the PROVER_NUMBER during the testing
    ---> PROVER_NUMBER are all the provers of the system
'''
DID_LIST_PROV = [2, 6, 50, 51, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22] # DID of provers that will ask for a Proof Of Location and a verify process
LOCATION_LIST_PROV = ["7H369F4W+Q8", "7H369F4W+Q8", "7H369F4W+Q8", "7H369F4W+Q8", "7H369F4W+Q9", "7H369F4W+Q9", "7H369F4W+Q9", "7H369F4W+Q9", "7H368FRV+FM", "7H368FRV+FM", "7H368FRV+FM", "7H368FRV+FM", "7H368FWV+X6", "7H368FWV+X6", "7H368FWV+X6", "7H368FWV+X6", "7H369FXP+FH"] # list of Provers locatios. Used for build the prover object


#### We know the position of every witness because it is stored in dictOfLocation. The position is the KEY, the values are the DID of user in that position
dictOfLocation = {
    "7H369FXP+FH":[
        0, 
        3,
        4,
        5
    ],
    "7H369F4W+Q8":[
        2,
        6,
        50,
        51
    ],
    "7H369F4W+Q9":[
        8,
        9,
        10,
        11
    ],
    "7H368FRV+FM":[ #Bologna
        12,
        13,
        14,
        15
    ],
    "7H368FWV+X6": [ #Ice-cream Bologna
        16,
        17,
        18,
        19
    ], 
    "7H369FXP+FH": [ # Ranzani 13: 44.4864416,11.3986586
        22,
        30,
        44,
        26
    ]
            
}

NUMBER_OF_LOCATIONS = 6 #number of different locations. For each location there could be a smart contract


class Witness:
    def __init__(self, did, public_key, private_key, proofs_array_computed, location):
        self.did = did
        self.public_key = public_key
        self.private_key = private_key
        self.proofs_array_computed = proofs_array_computed
        self.location = location
    
    '''
        This method will compute the proof when require from provers
    '''
    def comput_location_Prover(self, locationProver):
        # send proof
        pass
    
    '''
        This method allow to the witness to compute the distance from the prover.

        In the real case we'll use the bluetooth range, so this function might not exists.
    '''
    def computed_distance_from_prover(self, olc_witness, olc_prover):
        if (olc_witness == olc_prover):
            return True
        else:
            return False
        

class Prover(Witness):
    def __init__(self, did, account, private_key, proofs_array_computed, location, proofs_received_array, title_report, description_report, tx_id_data):
        super().__init__(did, account, private_key, proofs_array_computed, location)
        self.proofs_received_array = proofs_received_array
        self.title_report = title_report
        self.description_report = description_report
        self.tx_id_data = tx_id_data


    '''
        - writeDataOnBlockchain:  
            -> allow the prover to insert data in the blockchain encripting them with the verifier public key
            @input_params:
                * prover's passphase;
                * data to insert inside the transaction
    '''
    def writeDataOnBlockchain(self, passphase, title, description):
        data = [title, description]
        transaction_id = make_transaction(passphase, data)
        return transaction_id
    '''
        This method will return the list of neihbours. 
        listWitnessLocation is the input dict that own the location of every users:
            - the Key is the position OLC
            - the Value is a List of users DIDs, in a location can be many users that means many DIDs
    '''
    def find_neighbours(self, locationProver, dicWitnessLocation):
        if (dicWitnessLocation.get(locationProver)):
            tempListNeigh = dicWitnessLocation.get(locationProver)
            # need to copy the list in a new one to overcome the issue of "pass by reference"
            listNeighboursFound = tempListNeigh.copy()
            #print("zaas",listNeighboursFound)
            #count how many neighbours I have found
            numberOfNeighboursFound = len(listNeighboursFound)
            # remove the DID of the user that is making the request from the list; e.g. if the user with DID 2 make the request, the neighbour list could be [2,3,4,5,6], then I need to remove his DID from the list which is 2. The new list will be [3,4,5,6]
            listNeighboursFound.remove(self.did)
            
            if numberOfNeighboursFound >= 1:
                print("I have found ",numberOfNeighboursFound, " neighbours for user with DID ", self.did)
                return listNeighboursFound
            else:
                print("ERROR: no neighbours foud except you")
                return None
        else: 
            print('No Neighbours found in your location: ', locationProver)

    '''
        This method allow to the prover to compute the distance from the witness.

        In the real case we'll use the bluetooth range, so this function might not exists.
    '''
    def computed_distance_from_witness(self, olc_witness, olc_prover):
        super(Prover, self).computed_distance_from_prover(olc_witness, olc_prover)
        pass

    ''' 
        When a user want to send his location to the smart contract,
        we have to check if the location is already sent (checking inside the
        hypercube).
        
        If the location is still not sent, user will have to deploy the contract.
    '''
    def retrieve_position_hypercube(self):
        # Check hypercube

        # Deploy smart contract if location is not in the hypercube
        pass

    def createAccount(self, i):
        # ########### #######  WORK WITH REACH DEVNET ##################
        #acc_prover = rpc("/stdlib/newTestAccount", STARTING_BALANCE)


        
        # use newAccountFromMnemonic for Algorand testnet
        acc_prover = rpc("/stdlib/newAccountFromMnemonic", list_private_public_key[i])
      
        return acc_prover
        
    # this method will interact with index.py
    def deploySmartContract(self, proverObject):
        #rpc('/stdlib/setProviderByName','TestNet')
        ctc_creator = rpc("/acc/contract", proverObject.account)
        print("Smart contract deployed  🚀 :", ctc_creator)
        print("Inserting Creator's information into the contract ...")
        creatorThread = Thread(target=play_Creator, args=(ctc_creator, proverObject.location, proverObject.did, 'proof', proverObject.tx_id_data))
       
        return creatorThread, ctc_creator

    # this method will interact with index.py
    def attachToSmartContract(self, proverAttacherObject, ctc_creator):
        print("Calling play bob")
        attacherThread = Thread(target=play_bob, args=(ctc_creator, proverAttacherObject.account, proverAttacherObject.location, proverAttacherObject.did, 'proof', proverAttacherObject.tx_id_data))
        #attacherThread.start()
        print("playbob called successfully")
        return attacherThread



def createWitness(did, public_key, private_key, proofs_array_computed, location):
    wit = Witness(
        did= did, # Decentralized IDentifier 
        public_key= public_key, # Public key of the wallet
        private_key= private_key, # Private key of the wallet
        proofs_array_computed= proofs_array_computed, # Witness will store every proof that has computed for someone (in the local mobile db e.g Room Database with Android) 
        location= location)

    return wit

def createProver(did, account, private_key, proofs_array_computed, location, proofs_received_array, title_report, description_report, tx_id_data):
    prov = Prover(
        did= did,
        account= account,
        private_key= private_key,
        proofs_array_computed= proofs_array_computed,
        location= location,
        proofs_received_array= proofs_received_array,
        title_report=title_report,
        description_report=description_report,
        tx_id_data=tx_id_data) #store the received proofs
    
    return prov

''' 
    We'll use  Open Location Code format.
    This is ideally suited for people that live in rural areas and don’t have access to an address.
'''
def generateOLC(latitude, longitude):
    location_encoded = olc.encode(latitude, longitude) #lat - long - N° digits. Default is 10 digits which allow 14m of precisions
    print('Encoded location: ', location_encoded)
    return location_encoded


# START the simulation
def startSimulation():
    dict_location_sc = {} # keep track if the smart contract is newAccountFromMnemonicalready associated to this particular location. Its lenght will be equal to NUMBER_OF_LOCATIONS
    
    # Starting prover steps
    for i in range(0, PROVER_NUMBER): #for every prover of the entire system ...
        ##### TODO: Generate random LATITUDE & LONGITUDE (for every user), Then convert them to Open Location code and add to LOCATION_LIST_PROV
        #generateOLC(11.3474453,44.4930181 )#11.356988, 44.495888) # just for testing
        #buildDict()

        prov = createProver(
            did= DID_LIST_PROV[i], # The Prover ID come from an default array that contains all the IDs
            account= "None",
            private_key= "None",
            proofs_array_computed= [],
            location= LOCATION_LIST_PROV[i], # The Prover Location come from an default array that contains all the Locations
            proofs_received_array=[],
            title_report="Report Title here ...",
            description_report="Descrition of the report ...",
            tx_id_data="None")
        
        account_prov = prov.createAccount(i) #passing the number of prover to create
        # TODO: create a list of object provers and remove the two line below. Refactoring
        prover_list_account.append(account_prov)
        prover_addresses.append(format_address(account_prov)) #getting the wallet addresses for prover and appending to the list
        prov.account = account_prov

        #store data inside the blockchain
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     write_tx_thread = executor.submit(prov.writeDataOnBlockchain, list_private_public_key[i], prov.title_report, prov.description_report)
        #     tx_id = write_tx_thread.result()
        #     #print(tx_id)
        #     prov.tx_id_data = tx_id

        # Find neighbours
        neighbours = prov.find_neighbours(prov.location, dictOfLocation)
        if neighbours: 

            print('→ 🪪 Prover DID: ', prov.did,'\n 📍 Location: ', prov.location, '\n    Neighbours: ', neighbours,'\n',)

            '''
                TODO: HERE you'll have to check if the data are already located inside the hypercube.
                        The first user that call the contract has to deploy it;
                        the others will attach.
            '''
            #time.sleep(5)
            # the IF will simulate the initial check inside the hypercube. If the SC is not associated to a location in the hypercube (the dictionary in this case) then deploy a new smart contract and insert its ID and location inside the hypercube
            if (prov.location in dict_location_sc) == False: # if the location is not inserted inside the dict that track the SC deployed, then deploy a new smart contract and add the contract address to the dict 
                print(" Deploying the smart contract ...")
                creatorThread, contract_creator_deployed = prov.deploySmartContract(prov)
                creatorThread.start()
                prover_thread.append(creatorThread)
               
                '''
                    TODO: insert the required data inside the hypercube 
                '''

                dict_location_sc[prov.location] = contract_creator_deployed #insert the contract_id inside the dict_location_sc which track the contract deployed
            else:
                #print("\n User is attaching to the Smart contract ",dict_location_sc.get(prov.location),  " 🟩 📎 📎 🟩 ")
                retrieved_ctc = dict_location_sc[prov.location]
                print("User: ",format_address(prov.account)," Preparing the Attaching to the contract ...", retrieved_ctc)
                proverThread = prov.attachToSmartContract(prov, retrieved_ctc)

                proverThread.start()

                prover_thread.append(proverThread)
                

    # Joining the thread of provers and verifiers
    print("num threads: ",len(prover_thread))
    print("end_list (time)", end_list)

    wallet_pub_key  = [
        "GIM3KUP5473BIGGJZ3GNDREHC2YT2P4W4WJZXDILWLAYI57A4GAML33DRY",
        "O47RCDX6L725MCPKEQNWWCMZAMR3UNIUYSKKV7N5UEAZDC2A6HPPID4C7Q",
        "C5PCYMHJJPL5HBVL7KOJ5EXXNYOZCWYRKEP5NMNC6Z44CQLWABDDSZFBKI",
        "7EH36BDEHMHFYJUISRA4QZYIHCCN5U4ZEQ3Q64T7OAYSMIRARZ3Q6C6F3E",
        "5RW4HL5YY6FMYSICN5LYCCWM4LRXGNGJPU3RYW3SVRKADB7N2Z7OOIKZ7E",
        "X56EISCBSSPAS75S2RZFJVBEXMGCVI2WG4QMIHRRCAHUGTCUGF7RE6643M",
        "2PDAQC47IFBJNU5AETJA2OV3I6NKDF4AAIZRG72ALDXMAUCEOO4KZPOO4E",
        "BDFYNQR2I3YQR6WMTBYRYDJXCXDLIW5T22DVKT4IVL6R4ZQVI336E3VDNQ",
        "3YMI5U6ZKH3MZ3DNYWO3YL3SCH75KBBCWO2XOO2HEVFQSX3G2Y4UYPOWWA",
        "7TIHVKNIGJF5H37SJDWWKOOT4FRUE4XDUGCZ77HZVKAEAHAWKLSS2LXRUQ",
        "HKCHIEF5XKK6NYAYUBWHTX3JB7H62QQ36RWPUPNBGL75SXQB27ZWX5Q6DQ",
        "22X4O3I5FSGYK4XTMWL6OEPKX7FPBI3QH4BB42VIZ75J7GVUDJZYCJ56OA",
        "QF25BWUJIY3NDFS47EILAOV4DAAHIYC2PRVIGERSQVTJ7RXHY44QBA6KO4",
        "MJXSIP7ULI25QH3XJP7AVQT7ZYO3TARYVUYRD6ARR6L6HWGH22ECU5MHAE",
        "XSKXAH4SIWFOLFUWS6H73JUJ5HJOWUCBKTA6LFXFCYS6VDZMQL6RI5HGQM",
        "JI7VRGDIANFNABPJL6PWVGCP42NZGQVV7T3QVJD6P47EKQP2BXSFMPU7RA",
    ]

    time_delta_list = []
 
    for (i,t) in enumerate(prover_thread):
        t.join()
        delta = end_list[i]-start_list[i]
        time_delta_list.insert(i, delta)
        print("new delta: ", delta)

    for provUser in prover_list_account:
        rpc("/forget/ctc", provUser)


    print(time_delta_list)
    # plotting the time of deploy and transaction for each account
    height = time_delta_list
    bars = (wallet_pub_key)
    x_pos = np.arange(len(bars))
    plt.bar(x_pos, height)
    plt.xticks(x_pos, bars, rotation=90)
    plt.xlabel('Accounts')
    plt.ylabel('Seconds')  

    # Create names on the x-axis
    plt.xticks(x_pos, bars)

    # Show graphic
    plt.show()

            
def main():
    startSimulation()


if __name__ == '__main__':
    main()




