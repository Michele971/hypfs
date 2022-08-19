
from openlocationcode import openlocationcode as olc
from reach_rpc import mk_rpc
from index import format_address
from index import play_Creator, play_bob, verifier_pay, verifier_api_verify
from threading import Thread
import time
prover_thread = [] #list of prover thread
prover_list_account = [] #list of prover account 
prover_addresses = [] # list of provers addresses

verifier_addresses = [] #list of verifier thread
verifier_list_account = [] #list of verifier account 

contract_creator_deployed = None # contrat deployed, will have to be a list of contracts

rpc, rpc_callbacks = mk_rpc()
STARTING_BALANCE = rpc("/stdlib/parseCurrency", 1000) # use "parseCurrency" method when you send value TO backend
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

WITNESS_NUMBER = 4 # number of witnesses
PROVER_NUMBER = 5 # number of provers
DID_LIST_WIT = [0, 3, 4, 5] # list of DID witnesses
LOCATION_LIST_WIT = ["7H369FXP+FH", "7H369F4W+Q8", "7H369F4W+Q9"] # list of witnesses locations

'''
    ❗️❗️❗️❗️  WARNING: ❗️❗️❗️❗️
    ---> len(DID_LIST_PROV) and len(LOCATION_LIST_PROV) MUST TO BE EQUALS !!! You can decrease the PROVER_NUMBER during the testing
    ---> PROVER_NUMBER must be less or equal to SMART_CONTRACT_MAX_USER variable located inside index.rsh
'''
DID_LIST_PROV = [2, 6, 8, 14, 19] # DID of provers that will ask for a Proof Of Location and a verify process
LOCATION_LIST_PROV = ["7H369F4W+Q8", "7H369F4W+Q8", "7H369F4W+Q9", "7H368FRV+FM", "7H368FWV+X6"] # list of Provers locatios

VERIFIER_NUMBER = 1 #number of verifiers
DID_LIST_VER = [99] #list of DID associated to verifiers

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
        6
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
        14
    ],
    "7H368FWV+X6": [ #Ice-cream 
        15,
        16,
        17,
        18,
        19
    ],
  

}


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
        print(" ✅  ",proverToVerify," succesfully verified! ")
        return verifierThread

    def createAccount(self):
        acc_verifier = rpc("/stdlib/newTestAccount", STARTING_BALANCE)
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
            return dicWitnessLocation.get(locationProver)
        else: 
            print('No Neighbours found in your location: ', locationProver)

    def send_location(self):
        # return proof
        pass

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

    def createAccount(self):
        acc_prover = rpc("/stdlib/newTestAccount", STARTING_BALANCE)
        return acc_prover


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
'''
def generateOLC(latitude, longitude):
    location_encoded = olc.encode(latitude, longitude) #lat - long - N° digits. Default is 10 digits which allow 14m of precisions
    print('Encoded location: ', location_encoded)
    return location_encoded


# this method will interact with index.py
def deploySmartContract(proverObject):
    ctc_creator = rpc("/acc/contract", proverObject.account)
    creatorThread = Thread(target=play_Creator, args=(ctc_creator, proverObject.location, proverObject.did, 'proof',))
    creatorThread.start()
    return creatorThread, ctc_creator

# this method will interact with index.py
def attachToSmartContract(proverAttacherObject, ctc_creator):
    attacherThread = Thread(target=play_bob, args=(ctc_creator, proverAttacherObject.account, proverAttacherObject.location, proverAttacherObject.did, 'proof',))
    attacherThread.start()

    return attacherThread



# START the simulation
def startSimulation():
    global contract_creator_deployed 
    # Starting prover steps
    for i in range(0, PROVER_NUMBER):
        # bologna: 11.3411625, 44.4942452
        # la vecchia stalla gelateria: 11.3474453, 44.4930181 
        ##### TODO: Generate random LATITUDE & LONGITUDE (for every user), Then convert them to Open Location code and add to LOCATION_LIST_PROV
        #generateOLC
        #generateOLC(11.3474453,44.4930181 )#11.356988, 44.495888) # just for testing
        #buildDict()

        prov = createProver(
            did= DID_LIST_PROV[i], # The Prover ID come from an default array that contains all the IDs
            account= "FFFFFFFFF",
            private_key= "xxxxxxx",
            proofs_array_computed= [],
            location= LOCATION_LIST_PROV[i], # The Prover Location come from an default array that contains all the Locations
            proofs_received_array=[])

        account_prov = prov.createAccount()
        # TODO: create a list of object provers and remove the two line below. Refactoring
        prover_list_account.append(account_prov)
        prover_addresses.append(format_address(account_prov)) #getting the wallet addresses for prover and appending to the list
        prov.account = account_prov

        # Find neighbours
        neighbours = prov.find_neighbours(prov.location, dictOfLocation)
        if neighbours: 
            ### TODO: do not print the id of the prover!!
            print('→ 🪪 Prover DID: ', prov.did,'\n 📍 Location: ', prov.location, '\n    Neighbours: ', neighbours,'\n',)

            '''
                TODO: The first user that call the contract has to deploy it;
                    the others will attach.
            '''
            '''
                TODO: HERE you'll have to check if the data are already located inside the hypercube
            '''
            global location_in_hypercube
    
            
            time.sleep(3)
            if (location_in_hypercube == False):
                print(" Deploying the smart contract ...")
                creatorThread, contract_creator_deployed = deploySmartContract(prov)
                print("Smart contract deployed  🚀 ")
                prover_thread.append(creatorThread)
                '''
                    TODO: insert the required data inside the hypercube 
                '''

                location_in_hypercube = True # TODO: remove this in production
            else:
                proverThread = attachToSmartContract(prov, contract_creator_deployed)
                prover_thread.append(proverThread)
    

    # Starting Verifier steps
    '''
        ❗️  WARNING: ❗️
        ---> Check that SMART_CONTRACT_MAX_USER variable in index.rsh has been reached here: Everybody has to attach to the contract if you want going on with verifiers
    '''
    for i in range(0, VERIFIER_NUMBER):
        time.sleep(3)
        verifier = createVerifier(
            did= DID_LIST_VER[i],
            account= ""
        )
        #generate an account on blockchain for the verifier
        accountVerifier = verifier.createAccount()
        #assign the account to the verifier
        verifier.account = accountVerifier

        # is not mandatory, but the verifier can insert funds inside the smart contract
        print(" 💰💰  Verifier is going to insert funds inside the contract ...")
        verifier.paySmartContract(verifier, contract_creator_deployed)
        

        # verify some provers
        time.sleep(3)
        didProverToVerify = DID_LIST_PROV[1]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[1], didProverToVerify)

        time.sleep(3)
        didProverToVerify = DID_LIST_PROV[2]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[2], didProverToVerify)

        time.sleep(3)
        didProverToVerify = DID_LIST_PROV[3]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[3], didProverToVerify)

        time.sleep(3)
        didProverToVerify = DID_LIST_PROV[4]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[4], didProverToVerify)

        prover_addresses.remove(prover_addresses[1]) #remove the address from the provers that will need to be verify
        prover_addresses.remove(prover_addresses[1]) 
        prover_addresses.remove(prover_addresses[1]) 
        prover_addresses.remove(prover_addresses[1]) 

    # Joining the thread of provers and verifiers
    for provUser in prover_thread:
        provUser.join()
    
    for verifierUser in verifier_addresses:
        verifierUser.join()


    for provUser in prover_list_account:
        rpc("/forget/ctc", provUser)

    for verifierUser in verifier_list_account:
        rpc("/forget/ctc", verifierUser)
        
def main():
    startSimulation()


if __name__ == '__main__':
    main()







#### this method should build the input DICT in an automatic way 
# def buildDict():
#     list_temp_id_wit = []
#     list_temp_loc_wit = []
#     for i in range(0,WITNESS_NUMBER):
#         if wit[DID_LIST_WIT[i]]: #if exists
#             list_temp_id_wit.append(wit.get(DID_LIST_WIT[i]))
#         else:
#             list_temp_id_wit.append(DID_LIST_WIT[i])
#         wit = createWitness(  
#             did= list_temp_id_wit,
#             public_key= "SHJDAJAKRHAKD",
#             private_key= "xxxxx",
#             proofs_array_computed= [],
#             location= LOCATION_LIST_WIT[round(random.uniform(0, 1))])
      
#         list_temp_id_wit = []

       
#         #insert the witness in the dict of neighbours
#         dictOfLocation[list_temp_loc_wit[i]] = list_temp_id_wit[i] #TODO: FIX HERE --> THE VALUE MUST BE A LIST!!G
        

#     print(json.dumps(dictOfLocation, indent=4))

#     for i in range(0, PROVER_NUMBER):
#         prov = createProver(
#             did= DID_LIST_PROV[i],
#             public_key= "FFFFFFFFF",
#             private_key= "xxxxxxx",
#             proofs_array_computed= [],
#             location= LOCATION_LIST_PROV[round(random.uniform(0, 1))],
#             proofs_received_array=[])
        
#         # Find neighbours
#         locationProver = prov.location
#         neighbours = prov.find_neighbours(prov.location, dictOfLocation)
#         print('Hi Prover, your DID is: ', prov.did,'\n Your location is: ', prov.location, '\n Your neighbours are: ', neighbours)