
from platform import python_branch
from openlocationcode import openlocationcode as olc
from reach_rpc import mk_rpc
from index import format_address, get_balance
from index import play_Creator, play_bob, verifier_pay, verifier_api_verify
from threading import Thread
import time
import eth_new_account
from typing import List
import random

SMART_CONTRACT_MAX_USER = 3 # this is the same variable of index.rsh. They must be equals!

LOCATION_LIST_PROV = ["7H369F4W+Q8"]#, "7H369F4W+Q9"]#, "7H368FRV+FM", "7H368FWV+X6", "7H367FWH+9J", "7H368F5R+4V"] # list of Provers locatios. Used for build the prover object
PROVER_NUMBER = 4 # number of provers for the entire system

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
        rpc("/acc/setGasLimit", account_prov, 9000000) #9.000.000

        prover_addresses.append(format_address(account_prov))

        proversObjectList.append(prov)

        count += 1

    return proversObjectList

list_private_public_key = [
    '0xf641b77d995ebade72e5a96f065232d9057284581e6b3ef6cbc194896ce606fa',
    '0x9de62bf46a345f949b6e2f07088a626f07e84f7ca4269917188573a0b1d0be4b',
    '0x833170377ef9e0cac6ae75989fed851279b723d12cfa880023adff5f341c8ab0',
    '0xc291f9aea360cc6d09a5bc071af3ee5e29a18bee02f4d39ed9f50633c7863eb1',

    '0xb8b60ef412eeb95643e5701ec56b5fb11698d576e08127c33f893949386a5e45',  
    '0xafe6f14b10d9a6693f04ebc1bf2090b406a89ffdb97713c9bf122e961b46c39d',  
    '0x50e50c32c43bc3b55ed7cdffacc03780508fe20774f8255989ab971415271cf4',  
    '0x8778e9ea55646607d276cc9ac858097e4b9ad3bb171b1d0a96d98b32f298c760'
]

verifiers_private = [
    '0xc10cbcca7bd0970503e1e1f404cec87cca59b636aae4f5044370a79753401c15' #0x6636F7B4A4d9077DBa98F9A0237192B160277200
]


prover_thread = [] #list of prover thread
prover_list_account = [] #list of prover account 
prover_addresses = [] # list of provers addresses
contract_creator_deployed = None # contrat deployed, will have to be a list of contracts

verifier_thread = []

rpc, rpc_callbacks = mk_rpc()
#you can use the testnet
#rpc("/stdlib/setProviderByName","TestNet")
#or specify the URI
# rpc("/stdlib/setProviderByEnv",{
#         #"ETH_NODE_URI":"https://tiniest-neat-field.matic-testnet.discover.quiknode.pro/6cf11cc8bcbdde3b18c83f183958f440ae58b33f/"
#         #"ETH_NODE_URI":"https://sepolia.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e"
#         "ETH_NODE_URI":"https://goerli.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e"
#     }
# )
print("\t\t The consesus network is: ", rpc('/stdlib/connector'))

STARTING_BALANCE = rpc("/stdlib/parseCurrency", 1500) # use "parseCurrency" method when you send value TO backend
location_in_hypercube = False # simulate if the location is already stored in hypercube

'''
    NOTEs:
    - Since we don't simulate the bluetooth feature during the process that finds neighbors,
    we assume that if the Open Location Code, between two or more users, is the same, then the 
    distance is very small. To assume that, we'll have to use the default OLC precision of 10 digits
    which consist in a range of 14m.
    We are aware that users in two different squares can be close althought the OLC is different, however we
    don't simulate that.
'''

VERIFIER_NUMBER = 1 #number of verifiers
DID_LIST_VER = [99] #list of DID associated to verifiers


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
        
class Verifier():
    def __init__(self, did, account):
        self.did = did
        self.account = account
    
    #this method allow the verifier to attach and pay the smart contract
    def paySmartContract(self, verifierObject, ctc_creator):
        verifierThread = Thread(target=verifier_pay, args=(ctc_creator, verifierObject.account))
        verifierThread.start()

        return verifierThread
    
    #this method allow the verifier to verify a prover using "proverToVerify" variable and using the DID of the prover "didProver"
    def verifySmartContract(self, verifierObject, ctc_creator, proverToVerify, didProver):
        print(" Verifier is going to verify some provers ")
        verifierThread = Thread(target=verifier_api_verify, args=(ctc_creator,verifierObject.account, didProver, proverToVerify)) 
        verifierThread.start()
        return verifierThread

    def createAccount(self):
        acc_verifier = rpc("/stdlib/newTestAccount", STARTING_BALANCE)
        #acc_verifier = rpc("/stdlib/newAccountFromSecret", verifiers_private[0])

        return acc_verifier

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


    def createAccount(self, i):
        # ########### #######  WORK WITH REACH DEVNET ##################
        acc_prover = rpc("/stdlib/newTestAccount", STARTING_BALANCE)
    
        # ########### #######  WORK WITH ETHEREUM TESTNET ##################
        #acc_prover = rpc("/stdlib/newAccountFromSecret", list_private_public_key[i])
      
            
        return acc_prover
        
    # this method will interact with index.py
    def deploySmartContract(self, proverObject):
        ctc_creator = rpc("/acc/contract", proverObject.account)
        print(" ⏳⏳ Calling the deploying and starting the thread ...")
        creatorThread = Thread(target=play_Creator, args=(ctc_creator, proverObject.location, proverObject.did, 'proof',))
        
        return creatorThread, ctc_creator

    # this method will interact with index.py
    def attachToSmartContract(self, proverAttacherObject, ctc_creator):
        print(" ⏳ Calling the attach api and starting the thread ...")
        attacherThread = Thread(target=play_bob, args=(ctc_creator, proverAttacherObject.account, proverAttacherObject.location, proverAttacherObject.did, 'proof',))
        return attacherThread



def createWitness(did, public_key, private_key, proofs_array_computed, location):
    wit = Witness(
        did= did, # Decentralized IDentifier 
        public_key= public_key, # Public key of the wallet
        private_key= private_key, # Private key of the wallet
        proofs_array_computed= proofs_array_computed, # Witness will store every proof that has computed for someone (in the local mobile db e.g Room Database with Android) 
        location= location)

    return wit

def createProver(did, account, private_key, proofs_array_computed, location, proofs_received_array):
    prov = Prover(
        did= did,
        account= account,
        private_key= private_key,
        proofs_array_computed= proofs_array_computed,
        location= location,
        proofs_received_array= proofs_received_array) #store the received proofs
    
    return prov

def createVerifier(did, account):
    ver = Verifier(
        did= did,
        account= account
    )
    return ver
''' 
    We'll use  Open Location Code format.
    This is ideally suited for people that live in rural areas and don’t have access to an address.

    e.g. generateOLC(11.3474453,44.4930181)

'''
def generateOLC(latitude, longitude):
    location_encoded = olc.encode(latitude, longitude) #lat - long - N° digits. Default is 10 digits which allow 14m of precisions
    print('Encoded location: ', location_encoded)
    return location_encoded


# START the simulation
def startSimulation():
    #generate N random provers
    generate_prover_list = generateProvers(PROVER_NUMBER) # try with 8, 12, 16 etc.

    print("\n\n----------- START -----------")
    dict_location_sc = {} # keep track if the smart contract is already associated to this particular location. Its lenght will be equal to NUMBER_OF_LOCATIONS
    
    # Starting prover steps
    for i in range(0, PROVER_NUMBER): #for every prover of the entire system ...
        prov = generate_prover_list[i]
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
                print("\n")

            else:
                retrieved_ctc = dict_location_sc[prov.location]
                proverThread = prov.attachToSmartContract(prov, retrieved_ctc)
                proverThread.start()
                prover_thread.append(proverThread)
                

    # Starting Verifier steps
    '''
        ❗️  WARNING: ❗️
        ---> Check that SMART_CONTRACT_MAX_USER variable in index.rsh has been reached here: Everybody has to attach to the contract if you want going on with verifiers
    '''
    print("\n")
    print("\n\t ----- sleeping before verification process")
    time.sleep(30)
    print("Start the verification process")
    for i in range(0, VERIFIER_NUMBER):

        verifier = createVerifier(
            did= DID_LIST_VER[i],
            account= ""
        )
        #generate an account on blockchain for the verifier
        accountVerifier = verifier.createAccount()
        #assign the account to the verifier
        verifier.account = accountVerifier

        contract_creator_deployed = dict_location_sc.get('7H369F4W+Q8') # JUST FOR TESTING: verify 7H369F4W+Q8 contract
        # is not mandatory, but the verifier can insert funds inside the smart contract
        print(" 💰💰  Verifier is going to insert funds inside the contract ", contract_creator_deployed, ' ...')

        threadVer = verifier.paySmartContract(verifier, contract_creator_deployed)
        verifier_thread.append(threadVer)
        
        print("WAITING 50")
        # verify some provers
        time.sleep(20)

        didProverToVerify = mapping_list_did.get('7H369F4W+Q8')[0]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[0], didProverToVerify)
        print("Verifier is going to insert data in hypercube")

        print("WAITING 50")
        # verify some provers
        time.sleep(20)

        didProverToVerify = mapping_list_did.get('7H369F4W+Q8')[1]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[1], didProverToVerify)
        print("Verifier is going to insert data in hypercube")
        #TODO: insert data inside the hypercube


        print("WAITING 50 ...")
        time.sleep(20)
        didProverToVerify = mapping_list_did.get('7H369F4W+Q8')[2]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[2], didProverToVerify)

        time.sleep(20)
        didProverToVerify = mapping_list_did.get('7H369F4W+Q8')[3]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[3], didProverToVerify)
        '''
            verify the second smart contract
        '''
        # time.sleep(10)
        # contract_creator_deployed = dict_location_sc.get('7H369F4W+Q9') # JUST FOR TESTING
        # # is not mandatory, but the verifier can insert funds inside the smart contract
        # print(" 💰💰  Verifier is going to insert funds inside the contract ", contract_creator_deployed, ' ...')
        # print("verifier.account", verifier.account)
        # verifier.paySmartContract(verifier, contract_creator_deployed)
        

        # verify some provers
        # time.sleep(70)
        # didProverToVerify = DID_list[5]
        # verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[5], didProverToVerify)

        # time.sleep(70)
        # didProverToVerify = DID_list[6]
        # verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[6], didProverToVerify)

        # time.sleep(70)
        # didProverToVerify = DID_list[7]
        # verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[7], didProverToVerify)



    # START DEBUG 
    time.sleep(5)
    print("\t\t\t DEBUG INFORMATION")

    for provUser in prover_list_account:
        print("BALANCE OF ",format_address(provUser), " is ",get_balance(provUser))

    print("Contratto deployato: ",contract_creator_deployed)
    print("Account del verifier: ", format_address(verifier.account))
    print("Balance del verifier: ", get_balance(verifier.account))
    #END DEBUG

    # Joining the thread of provers and verifiers
    for provUser in prover_thread:
        provUser.join()


    for verifierUser in verifier_thread:
        verifierUser.join()


    for provUser in prover_list_account:
        rpc("/forget/ctc", provUser)


        
def main():
    startSimulation()


if __name__ == '__main__':
    main()





