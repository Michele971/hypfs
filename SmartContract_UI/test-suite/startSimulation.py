
from platform import python_branch
from openlocationcode import openlocationcode as olc
from reach_rpc import mk_rpc
from index import format_address
from index import play_Creator, play_bob
from threading import Thread
import time
import eth_new_account
from index import start_list, end_list
import numpy as np
import matplotlib.pyplot as plt
import random
'''
    ---------------------------------------------------------------------------------------
    ------------------    THIS SCRIPT MUST BE RUN ON ETHEREUM TESTNET    ------------------
    ---------------------------------------------------------------------------------------
'''

SMART_CONTRACT_MAX_USER = 3 # this is the same variable of index.rsh. They must be equals!

LOCATION_LIST_PROV = ["7H369F4W+Q8", "7H369F4W+Q9", "7H368FRV+FM", "7H368FWV+X6"]#, "7H367FWH+9J", "7H368F5R+4V"] # list of Provers locatios. Used for build the prover object
PROVER_NUMBER = 16 # number of provers for the entire system

assert(PROVER_NUMBER/len(LOCATION_LIST_PROV) == 4) #There must be (SMART_CONTRACT_MAX_USER+1) users for each location. So increase the number of locations in LOCATION_LIST_PROV, or decrease the PROVER_NUMBER

DID_list = [] #will be fill at runtime
mapping_list_did = {} #will be fill at runtime

'''
    This method will generate n° prover objects setting their attribute such as DID, location or the consensus network account.
    The DID created will be unique.
    This method will create mapping_list_did dictionary, which will be used to check the users nearby.
'''
def generateProvers(n_users_to_generate):
    proversObjectList = []
    count = 0
    for i in range(n_users_to_generate):
        #use to assign each ID to the location
        if count == len(LOCATION_LIST_PROV):
            count = 0

        # choose the location from the list of locations
        chooseLocation = LOCATION_LIST_PROV[count] #there are SMART_CONTRACT_MAX_USER + 1 elements for each location. So: 0 < count <= (SMART_CONTRACT_MAX_USER+1)
        goOn = True
        #generate a random ID that does not still exists
        while goOn == True:
            DID_generated = random.randint(0, 100)
            if DID_generated not in DID_list:
                DID_list.append(DID_generated)
                goOn = False
            else:
                goOn = True

        # update the map that keep track of the locations and their users 
        mapping_list_did.setdefault(chooseLocation,[]).append(DID_generated) #the dict will be used to find the neighbours and othe operations

        #create a Prover object
        prov = createProver(
            did= DID_generated, 
            account= "Noone",
            private_key= "None",
            proofs_array_computed= [],
            location= chooseLocation, 
            proofs_received_array=[])
        
        #update some attributes of the prover objects
        account_prov = prov.createAccount(i) #passing the number of prover to create
        prover_list_account.append(account_prov)
        prov.account = account_prov
        rpc("/acc/setGasLimit", account_prov, 5000000)

        prover_addresses.append(format_address(account_prov))

        proversObjectList.append(prov)

        count += 1

    return proversObjectList


list_private_public_key = [
    '0xf641b77d995ebade72e5a96f065232d9057284581e6b3ef6cbc194896ce606fa',
    '0x9de62bf46a345f949b6e2f07088a626f07e84f7ca4269917188573a0b1d0be4b',
    '0x833170377ef9e0cac6ae75989fed851279b723d12cfa880023adff5f341c8ab0',
    '0xc291f9aea360cc6d09a5bc071af3ee5e29a18bee02f4d39ed9f50633c7863eb1',

    '0xb8b60ef412eeb95643e5701ec56b5fb11698d576e08127c33f893949386a5e45', # 0x5381113B7b13c15af3a534065001EdeB2476802c
    '0xafe6f14b10d9a6693f04ebc1bf2090b406a89ffdb97713c9bf122e961b46c39d', # 0xA6Abd9eB42aad1b98c2a9dF0B4E2E3c743162ba5
    '0x50e50c32c43bc3b55ed7cdffacc03780508fe20774f8255989ab971415271cf4', # 0x87985fC3dCE979C09E3c3e745A7A0B464540CA82
    '0x8778e9ea55646607d276cc9ac858097e4b9ad3bb171b1d0a96d98b32f298c760', # 0x1fE37BD94109bA874a235B44fA79fC2d7710F1B0

    '0x9e5cd974573308612579e29c2f1ba9899c5622cd273bcc00941acdb107260199',
    '0x12f576f887df544a76fbd88a79dafc852b9900e328b2a448450bc5fe4b60589a',
    '0xf285e21ad35d451453a0e11f1c2580316a66b74126528303f52d93dfa9d1dee3',
    '0x31c2d8d88b2de858e6a76f35b410bf68f24d9033a6d549111e12a91974895f3e',

    '0x1cb11272fb93f95c3e1e1be4158732133350eba49df1e5fe13adb06a572066dd',
    '0xd35e2d01b9a22f00a84af71642aecf79ea9c7c84cbcba9171ba96a2555245ad7',
    '0x1aea64ed14d59cc0daf0f0a9df7f00ff0f5382bb548ca1b12e293b3e4ed6c638',
    '0xa8f490477bdff610b4bc6ed10c6859e370c5d56c747253f7bfa8253b64b26840'
]


prover_thread = [] #list of prover thread
prover_list_account = [] #list of prover account 
prover_addresses = [] # list of provers addresses


contract_creator_deployed = None # contrat deployed, will have to be a list of contracts

rpc, rpc_callbacks = mk_rpc()
#rpc("/stdlib/setProviderByName","TestNet")
rpc("/stdlib/setProviderByEnv",{
    "ETH_NODE_URI":"https://tiniest-neat-field.matic-testnet.discover.quiknode.pro/6cf11cc8bcbdde3b18c83f183958f440ae58b33f/"
    # "ETH_NODE_URI":"https://sepolia.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e"
    #"ETH_NODE_URI":"https://goerli.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e"
    }
)

print("\t\t The consesus network is: ", rpc('/stdlib/connector'))


#STARTING_BALANCE = rpc("/stdlib/parseCurrency", 1500)  # only  for devnet

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
    def __init__(self, did, account, private_key, proofs_array_computed, location, proofs_received_array):
        super().__init__(did, account, private_key, proofs_array_computed, location)
        self.proofs_received_array = proofs_received_array

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
            #count how many neighbours I have found
            numberOfNeighboursFound = len(listNeighboursFound)

            # remove the DID of the user that is making the request from the list; 
            # e.g. if the user with DID 2 make the request, the neighbour list could be [2,3,4,5,6],
            #  then I need to remove his DID from the list which is 2. The new list will be [3,4,5,6]
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

    def createAccount(self, i):
        # ########### #######  WORK WITH REACH DEVNET ##################
        #acc_prover = rpc("/stdlib/newTestAccount", STARTING_BALANCE)
        
        # ########### #######  WORK WITH ETHEREUM TESTNET ##################
        acc_prover = rpc("/stdlib/newAccountFromSecret", list_private_public_key[i])

        return acc_prover
        
    # this method will interact with index.py
    def deploySmartContract(self, proverObject):
        ctc_creator = rpc("/acc/contract", proverObject.account)
        print("Smart contract deployed  🚀 :", ctc_creator)
        print("Inserting Creator's information into the contract ...")
        creatorThread = Thread(target=play_Creator, args=(ctc_creator, proverObject.location, proverObject.did, 'proof',))

       
        return creatorThread, ctc_creator

    # this method will interact with index.py
    def attachToSmartContract(self, proverAttacherObject, ctc_creator):
        #print("Calling play bob")
        attacherThread = Thread(target=play_bob, args=(ctc_creator, proverAttacherObject.account, proverAttacherObject.location, proverAttacherObject.did, 'proof',))

        #print("playbob called successfully")
        return attacherThread




def createProver(did, account, private_key, proofs_array_computed, location, proofs_received_array):
    prov = Prover(
        did= did,
        account= account,
        private_key= private_key,
        proofs_array_computed= proofs_array_computed,
        location= location,
        proofs_received_array= proofs_received_array) #store the received proofs
    
    return prov


''' 
    We'll use  Open Location Code format.
    This is ideally suited for people that live in rural areas and don’t have access to an address.
'''
def generateOLC(latitude, longitude):
    location_encoded = olc.encode(latitude, longitude) #lat - long - N° digits. Default is 10 digits which allow 14m of precisions
    print('Encoded location: ', location_encoded)
    return location_encoded

def fmt(x):
    return rpc("/stdlib/formatCurrency", x, 4)

def get_balance(w):
    return fmt(rpc("/stdlib/balanceOf", w))

# START the simulation
def startSimulation():
    #generate N random provers
    generate_prover_list = generateProvers(PROVER_NUMBER) # try with 8, 12, 16 etc.

    first_test = 0

    print("\n\n----------- START -----------")
    dict_location_sc = {} # keep track if the smart contract is newAccountFromMnemonicalready associated to this particular location. Its lenght will be equal to NUMBER_OF_LOCATIONS

    # Starting prover steps
    for i in range(0, PROVER_NUMBER): #for every prover of the entire system ...
        ##### TODO: Generate random LATITUDE & LONGITUDE (for every user), Then convert them to Open Location code and add to LOCATION_LIST_PROV
        #generateOLC(11.3474453,44.4930181 )#11.356988, 44.495888) # just for testing

        prov = generate_prover_list[i]

        print("BALANCE: ",get_balance(prov.account))

        # Find neighbours
        neighbours = prov.find_neighbours(prov.location, mapping_list_did)
        if neighbours: 
            print('→ 🪪 Prover DID: ', prov.did,'\n 📍 Location: ', prov.location, '\n    Neighbours: ', neighbours,'\n',)

            '''
                TODO: HERE you'll have to check if the data are already located inside the hypercube.
                        The first user that call the contract has to deploy it;
                        the others will attach.
            '''
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
                if first_test == 0:
                    print("\n\n\tsleeping test 10 secs")
                    #time.sleep(700)
                    first_test = 1
                retrieved_ctc = dict_location_sc[prov.location]
                #print("User: ",format_address(prov.account)," Preparing the Attaching to the contract ...", retrieved_ctc)
                proverThread = prov.attachToSmartContract(prov, retrieved_ctc)

                proverThread.start()
                prover_thread.append(proverThread)
                

    # Joining the thread of provers and verifiers
    print("num threads: ",len(prover_thread))
    print("end_list (time)", end_list)



    wallet_pub_key = [
        '0x34c17b647dDd4E38CDC2F5B38efd1F42681cB889',
        '0xF8f1AAcEDf0dBB07693f76e807e4EF9a96A6Aa9f',
        '0xAc18Ec4c7f390663B179a7891f26247612654c8c',
        '0x91EF6D0F7c12b5FF0c1F81DCFFAF1e30BF0F52D7',

        '0x5381113B7b13c15af3a534065001EdeB2476802c',
        '0xA6Abd9eB42aad1b98c2a9dF0B4E2E3c743162ba5',
        '0x87985fC3dCE979C09E3c3e745A7A0B464540CA82',
        '0x1fE37BD94109bA874a235B44fA79fC2d7710F1B0',

        '0xfbe72863099f8fCAFe6Df5626692013Ce2e83ec3',
        '0x7e90fCc0B6a4459A2c47A2b015c37fB5340aCcb5',
        '0xC4A9067cE5542899510e6cB8A2Eb84A0a0953eDE',
        '0x63d3e6E0d2E762570819086f3E6dEF5061a27890',

        '0x7b3180CFeBc06f78Cc55D2bA19cA24dfa2d1fe44',
        '0x9F81B843da3c2d66b08d7Af60c1FE7D79e20771E',
        '0xf71Fea9ED70597c365B5D8A2bD78e04E31654c5e',
        '0x1aF193411dDf746C501459406e8f00f465E11433'

    ]

    time_delta_list = []
 
    for (i,t) in enumerate(prover_thread):
        t.join()
        delta = end_list[i]-start_list[i]
        time_delta_list.insert(i, delta)
        print("new delta: ", delta)
        


    for provUser in prover_list_account:
        rpc("/forget/ctc", provUser)


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
    #plt.show()

    plt.savefig('./outputPerformance.png')
    


def main():
    startSimulation()


if __name__ == '__main__':
    main()




