
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

LOCATION_LIST_PROV = ["7H369F4W+Q8", "7H369F4W+Q9"]#, "7H368FRV+FM", "7H368FWV+X6", "7H367FWH+9J", "7H368F5R+4V"] # list of Provers locatios. Used for build the prover object
PROVER_NUMBER = 8 # number of provers for the entire system

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
        prov.account = account_prov
        rpc("/acc/setGasLimit", account_prov, 5000000)

        prover_addresses.append(format_address(account_prov))

        proversObjectList.append(prov)

        count += 1

    return proversObjectList


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
    '0x3888a91f2bae15a5c8df4545ecc2b2a50ea2f0034ec168df7ae429987eabf405',
    '0xf5568735c8cb26c544944dc1e6025dd94c9a9d7f7422ea8168f417167d513867',
    '0x512981281c472444fa4d8b73866cc2b1235424bec8129eb448661c36134ff8ac',

    '0x8daea43f6969c5af179e890a2b05d7bbe4e65f33eaae2b1bacc12e70da03ab3e',
    '0x58db0a6d84722ba10fb1b6f57c127b9858c4d5be2c15ff9d15d6c9173dcaca86',
    '0xa8597bc7404aa73371e6631e4471eb9d10204a5622fe3441a657bd226a296c8b',
    '0xafea88fd0911cbd04c2755d02792951da04bd542e0243e6e6cba2d2a0becb804',

    '0x2a2f8106946f72489c73de1615c75a01cc7ea01167af3bdc7d85ec39067df728',
    '0xcaf6a8ddbd47dcd58f46ae5b5dcc2158ab63efc5c485c87dd87299e14621cd90',
    '0xb1b0b5b9a147a1b9c1368e34d6e66f347ce73b20c49543e3943e42e90f608322',
    '0xd62941f0dea36bf8f4f65c603adcd6eba881276e883caeea1b693961a5b1018f',

    '0x727f53bb6985612015ee07c19dd8d000a5a0786581b2a664cb909c3204a0e517',
    '0x5c677c0d81505f99b36cc3db9bdcae3d8296de0e70a5b98a628ee76fb1edcce3',
    '0xb70e021693dc22605961131f7cebac24020c25961d07e195fd13bd41900f441e',
    '0xbc6b37148c9032a04a0890a0e3f3ff2e93a58ee9d1f90e5031b9bec9cb40bfc5'
]


prover_thread = [] #list of prover thread
prover_list_account = [] #list of prover account 
prover_addresses = [] # list of provers addresses


contract_creator_deployed = None # contrat deployed, will have to be a list of contracts

rpc, rpc_callbacks = mk_rpc()
rpc("/stdlib/setProviderByName","TestNet")
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
        "0x832e977393410e0388f994bb773d78E83Ae9619E",
        "0x119d2BA2e52e21A88210Cd29DA0c7d45D2AC077A",
        "0xf373B8b4BcDEbD88efC8396b5420A41fE7c94011",
        "0x1eAd4c7aa92bABF7c923a8E597972CB3255Ab6C2",

        "0xe648143d83F7dD8eaaD587B9DDE0E40b7eFE0d62",
        "0x7211170e1CF574642857f98f7afA14990C39c75c",
        "0xC57D9AD7164af80AC324081D2A206179F567fECE",
        "0xBAa6cD46581b66E379c3B5436fa678976B34A518"

        # '0x6dd3FdD9752c5f935F1bF88542ab26D65eAC2B40',
        # '0x4c992e7D1fBfBa8Cd4cc429C5d1105ACbd9BAC45',
        # '0x5a2a37163523509Dee3B48D6740E5F25A8654Cb6', 
        # '0x5DE99700870d455DF99B3afCa0e7Cd85e8fF2f3d', 

        # '0x0E6ccE4c7C1AA5057c01c9c776168dC412d593f4', 
        # '0x199986ccBe425ef98a53C373A579b0d64F5daD3D', 
        # '0xA7953c30BD1Ae955ed19C162B0AEc2483c51c73D', 
        # '0x16C09e450A17B6De918D6637343700d7C6dB5d0d',
       
        # '0x1756CF5d7fac449F9211e41D3683E2f98b6f212c',
        # '0xF46eB2383D5FAe3C08916EB033A897C9E4de42bc',
        # '0x22eF5FE989C23D8F1136FE37Dc98d1Dd6b399145',
        # '0x350f42E342a573bFE301523C2Ec124a85109E318',
            
        # '0xf65B5f4066ea0Db43C0acc66bd9D3374065f9261',
        # '0xe68308bC0451fb9DD87084E9c6f04D0475AD1C56',
        # '0xBA3118B38cF737657d186efCd9827519E941cd31',
        # '0x0A1988095FD99756453DFFbB22a2154725eAF658' 
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




