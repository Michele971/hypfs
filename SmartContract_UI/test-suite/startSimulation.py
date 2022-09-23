
from platform import python_branch
from openlocationcode import openlocationcode as olc
from reach_rpc import mk_rpc
from index import format_address, get_balance
from index import play_Creator, play_bob, verifier_pay, verifier_api_verify
from threading import Thread
import time
import eth_new_account
from typing import List

list_private_public_key = [
    '0x8d10e8fb1aa289828f31914f581dbc39d9ed76b2e2d1247c49f5814349ff10c0', 
    '0x9cf648f6aaa283e0c227f9047e735e1d604875ce735223c334f1c511a0dd2b1b',
    '0xd1d2862447f71d78ab4d0b92800034c11cb7bd13ffe5d0a5bc2851e95ce719d7',
    '0x0fcab881cf4b6d40fbf1473b908d9501524b0d84ac7fe44196e763b8bde9545a',
    '0x18c78ad1e9447f077611e1945579c4215bb5551852e8b4957c89b783eb1aa3c8',
    '0x3c5baad76449c59aa1cff6d27febaa201d5150b86b382451d3645d8afd919a63',
    '0xc662ab78a9180104c1d20f9eb1f993794c093e98e7efe78e23d5ccb02fec637f',
    '0xbd0c0a94a5998144da5a64c5ca9c67cc92d383762fa58b7e8017eed63de908b4',
    '0x8ad4d716b3ed5c31cf4125fed2f9549259768482941f7ea3969d0fda93413e06',
    '0x3888a91f2bae15a5c8df4545ecc2b2a50ea2f0034ec168df7ae429987eabf405'
]

verifiers_private = [
    '0xc10cbcca7bd0970503e1e1f404cec87cca59b636aae4f5044370a79753401c15' #0x6636F7B4A4d9077DBa98F9A0237192B160277200
]


prover_list_account = [] #list of prover account 
prover_thread = [] #list of prover thread
prover_addresses = [] # list of provers addresses

verifier_addresses = [] #list of verifier thread
verifier_list_account = [] #list of verifier account 

contract_creator_deployed = None # contrat deployed, will have to be a list of contracts

rpc, rpc_callbacks = mk_rpc()
#rpc("/stdlib/setProviderByName","TestNet")

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
    - Every Smart Contract must have 4 Provers: 1 Creator - 3 user-prover. So, the variable inside backend SMART_CONTRACT_MAX_USER is equal to 3 (number of user nearby)
'''

WITNESS_NUMBER = 4 # number of witnesses
PROVER_NUMBER = 8 # number of provers for the entire system
DID_LIST_WIT = [0, 3, 4, 5] # list of DID witnesses
LOCATION_LIST_WIT = ["7H369FXP+FH", "7H369F4W+Q8", "7H369F4W+Q9"] # list of witnesses locations

'''
    ❗️❗️❗️❗️  WARNING: ❗️❗️❗️❗️
    ---> len(DID_LIST_PROV) and len(LOCATION_LIST_PROV) MUST TO BE EQUALS !!! You can decrease the PROVER_NUMBER during the testing
    ---> PROVER_NUMBER are all the provers of the system
'''
DID_LIST_PROV = [2, 6, 50, 51, 8, 9, 10, 11, 14, 19] # DID of provers that will ask for a Proof Of Location and a verify process
LOCATION_LIST_PROV = ["7H369F4W+Q8", "7H369F4W+Q8", "7H369F4W+Q8", "7H369F4W+Q8", "7H369F4W+Q9", "7H369F4W+Q9", "7H369F4W+Q9", "7H369F4W+Q9", "7H368FRV+FM", "7H368FWV+X6"] # list of Provers locatios. Used for build the prover object

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
        14
    ],
    "7H368FWV+X6": [ #Ice-cream Bologna
        15,
        16,
        17,
        18,
        19
    ],
}

NUMBER_OF_LOCATIONS = 5 #number of different locations. For each location there could be a smart contract


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
        # print(" ✅  ",proverToVerify," succesfully verified! ")
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
        acc_prover = rpc("/stdlib/newTestAccount", STARTING_BALANCE)


        
        #print("PRIVATE KEY: ", list_private_public_key[i])
        # ########### #######  WORK WITH ETHEREUM TESTNET ##################
        #acc_prover = rpc("/stdlib/newAccountFromSecret", list_private_public_key[i])
      

        #print("aaaaaaaaaa",rpc('/stdlib/providerEnvByName'))
        # consensus_network = rpc('/stdlib/providerEnvByName')
        # if consensus_network == 'ETH':
        #     #passphase_inserted = "coyote usual trigger laundry industry spoon quantum lyrics candy hood balance spell"
        #     private_key = "0x25db347fdf2ac94fa4e5893299bac50c81a091c3d12bc54f72716f2c692a5fef"
        #     acc_prover = rpc("/stdlib/newAccountFromSecret", private_key)

        # else consensus_network == 'ALGO':
        #         acc_prover = rpc("/stdlib/newAccountFromMnemonic", passphase_inserted)

            
        return acc_prover
        
    # this method will interact with index.py
    def deploySmartContract(self, proverObject):
        #rpc('/stdlib/setProviderByName','TestNet')
        ctc_creator = rpc("/acc/contract", proverObject.account)
        print("Smart contract deployed  🚀 :", ctc_creator)
        print("Inserting Creator's information into the contract ...")
        creatorThread = Thread(target=play_Creator, args=(ctc_creator, proverObject.location, proverObject.did, 'proof',))
        #creatorThread.start()
        
        return creatorThread, ctc_creator

    # this method will interact with index.py
    def attachToSmartContract(self, proverAttacherObject, ctc_creator):
        print("Calling play bob")
        attacherThread = Thread(target=play_bob, args=(ctc_creator, proverAttacherObject.account, proverAttacherObject.location, proverAttacherObject.did, 'proof',))
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





# START the simulation
def startSimulation():
    dict_location_sc = {} # keep track if the smart contract is already associated to this particular location. Its lenght will be equal to NUMBER_OF_LOCATIONS
    
    '''
        TODO: here START the timer for the DEPLOYING and INSERTING phase
    '''

    # Starting prover steps
    for i in range(0, PROVER_NUMBER): #for every prover of the entire system ...
        ##### TODO: Generate random LATITUDE & LONGITUDE (for every user), Then convert them to Open Location code and add to LOCATION_LIST_PROV
        #generateOLC(11.3474453,44.4930181 )#11.356988, 44.495888) # just for testing
        #buildDict()

        prov = createProver(
            did= DID_LIST_PROV[i], # The Prover ID come from an default array that contains all the IDs
            account= "FFFFFFFFF",
            private_key= "xxxxxxx",
            proofs_array_computed= [],
            location= LOCATION_LIST_PROV[i], # The Prover Location come from an default array that contains all the Locations
            proofs_received_array=[])

        account_prov = prov.createAccount(i) #passing the number of prover to create
        # TODO: create a list of object provers and remove the two line below. Refactoring
       
        prover_list_account.append(account_prov)
        prover_addresses.append(format_address(account_prov)) #getting the wallet addresses for prover and appending to the list
        prov.account = account_prov


        print("BALANCE OF ",format_address(account_prov), " is ",get_balance(account_prov))

        
        #setting the gas limit
        rpc("/acc/setGasLimit", account_prov, 5000000) # this line avoid the error displayed on etherscan which is: "out of gas"
   
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
                print("\n")
                #print("startint the creato sleep ...")
                #time.sleep(150)
            else:
                #print("\n User is attaching to the Smart contract ",dict_location_sc.get(prov.location),  " 🟩 📎 📎 🟩 ")
                retrieved_ctc = dict_location_sc[prov.location]
                print("User: ",format_address(prov.account)," Preparing the Attaching to the contract ...", retrieved_ctc)
                proverThread = prov.attachToSmartContract(prov, retrieved_ctc)
                #print("starting the sleep ...")
                #time.sleep(60)
                #print("Attach terminated")
                proverThread.start()
                prover_thread.append(proverThread)
                
    '''
        TODO: here STOP the timer for the DEPLOYING and INSERTING phase
    '''      
    
    '''
        TODO: here START the timer for the VERIFY phase
    '''
    # Starting Verifier steps
    '''
        ❗️  WARNING: ❗️
        ---> Check that SMART_CONTRACT_MAX_USER variable in index.rsh has been reached here: Everybody has to attach to the contract if you want going on with verifiers
    '''
    # DEBUG
    print("DICT: ", dict_location_sc)
    # END DEBUG

    time.sleep(35)
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
        print("verifier.account", verifier.account)
        verifier.paySmartContract(verifier, contract_creator_deployed)
        

        # verify some provers
        time.sleep(10)
        didProverToVerify = DID_LIST_PROV[1]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[1], didProverToVerify)

        time.sleep(10)
        didProverToVerify = DID_LIST_PROV[2]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[2], didProverToVerify)

        time.sleep(3)
        didProverToVerify = DID_LIST_PROV[3]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[3], didProverToVerify)
        '''
            verify the second smart contract
        '''
        time.sleep(3)
        contract_creator_deployed = dict_location_sc.get('7H369F4W+Q9') # JUST FOR TESTING
        # is not mandatory, but the verifier can insert funds inside the smart contract
        print(" 💰💰  Verifier is going to insert funds inside the contract ", contract_creator_deployed, ' ...')
        print("verifier.account", verifier.account)
        verifier.paySmartContract(verifier, contract_creator_deployed)
        

        # verify some provers
        time.sleep(3)
        didProverToVerify = DID_LIST_PROV[5]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[5], didProverToVerify)

        time.sleep(3)
        didProverToVerify = DID_LIST_PROV[6]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[6], didProverToVerify)

        time.sleep(3)
        didProverToVerify = DID_LIST_PROV[7]
        verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[7], didProverToVerify)


        # time.sleep(3)
        # didProverToVerify = DID_LIST_PROV[3]
        # verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[3], didProverToVerify)

        # time.sleep(3)
        # didProverToVerify = DID_LIST_PROV[4]
        # verifier.verifySmartContract(verifier, contract_creator_deployed, prover_addresses[4], didProverToVerify)

        #prover_addresses.remove(prover_addresses[1]) #remove the address from the provers that will need to be verify
        #prover_addresses.remove(prover_addresses[1]) 
        # prover_addresses.remove(prover_addresses[1]) 
        # prover_addresses.remove(prover_addresses[1]) 


    '''
        TODO: here STOP the timer for the VERIFY phase
    '''
    time.sleep(10)
    # DEBUG
    for provUser in prover_list_account:
        print("BALANCE OF ",format_address(provUser), " is ",get_balance(provUser))

    #END DEBUG

    # Joining the thread of provers and verifiers
    for provUser in prover_thread:
        provUser.join()


    for verifierUser in verifier_addresses:
        print("sono quiii verifier join!")
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