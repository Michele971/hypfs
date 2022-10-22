
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
import numpy as np
'''
    ---------------------------------------------------------------------------------------
    ------------------    THIS SCRIPT MUST BE RUN ON ETHEREUM TESTNET    ------------------
    ---------------------------------------------------------------------------------------
'''

SMART_CONTRACT_MAX_USER = 3 # this is the same variable of index.rsh. They must be equals!

LOCATION_LIST_PROV = ["7H369F4W+Q8", "7H369F4W+Q9", "7H368FRV+FM", "7H368FWV+X6", "7H367FWH+9J", "7H368F5R+4V", "7H369FXP+FH", "7H369F2W+3R"] # list of Provers locatios. Used for build the prover object
PROVER_NUMBER = 32 # number of provers for the entire system

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
        rpc("/acc/setGasLimit", account_prov, 8000000)

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
    '0xf285e21ad35d451453a0e11f1c2580316a66b74126528303f52d93dfa9d1dee3',
    '0x31c2d8d88b2de858e6a76f35b410bf68f24d9033a6d549111e12a91974895f3e',

    '0x9e5cd974573308612579e29c2f1ba9899c5622cd273bcc00941acdb107260199',
    '0x12f576f887df544a76fbd88a79dafc852b9900e328b2a448450bc5fe4b60589a',
    '0x50e50c32c43bc3b55ed7cdffacc03780508fe20774f8255989ab971415271cf4', # 0x87985fC3dCE979C09E3c3e745A7A0B464540CA82
    '0x8778e9ea55646607d276cc9ac858097e4b9ad3bb171b1d0a96d98b32f298c760', # 0x1fE37BD94109bA874a235B44fA79fC2d7710F1B0

    '0x1cb11272fb93f95c3e1e1be4158732133350eba49df1e5fe13adb06a572066dd',
    '0xd35e2d01b9a22f00a84af71642aecf79ea9c7c84cbcba9171ba96a2555245ad7',
    '0x1aea64ed14d59cc0daf0f0a9df7f00ff0f5382bb548ca1b12e293b3e4ed6c638',
    '0xa8f490477bdff610b4bc6ed10c6859e370c5d56c747253f7bfa8253b64b26840',

    '0x46fca04375b753148d711abd1f00e370d9a4da8d612b2d0e9f8799290028df90',
    '0x6f2467cf0dc2b02757ca25ab0c9e112971637e45249075fc78074c0a5cff6206',
    '0xbf39de3dfca255ecc39d786d1e74eb0ac7995db651258f061d1dbb56f7c62b1d',
    '0xd1912941d3f6ecd9d55bd5fc7408790ae6cc3f2dfb7d037e867bac2707436cbf',

    '0x16e2f555ace3ac16266a406ce44484578a4a856cc94a9122828fb002e3588672',
    '0xb4180e90b27d9b6f0b49b7213f11dfaaa575b03ada1e68de0a4f3017f93cfc87',
    '0x4237e0ad41e03dd26c40a6e9a3856161ef040cef4fc68beea788a8c4bbfd5b56',
    '0x8ed2c32dffbd3fee83ae8dddef2e2cb33de835a6e891f3ff1d5a6a3a8c593c49',

    '0x5e77ab5b1e4906f34c71105ca643094bf334725de500ed9f27e0df67789570d8',
    '0xd4df99e352af56e38ee7a52c69429156bd3f704d00af5a0240f1607343eaf0b6',
    '0xc067778224511bf27e2b9434662e1a6e74444db4a709dea3a52ef9709d8856f9',
    '0x8a27f845ad42d04624aa1e61af005f283864d6ffe3a61213adadb87689a36b5b',

    '0xf4f9a7b34c361b24265e01089b97ffb2823cf51d996331bcbcff46f91083ea8c',
    '0x953431fa1ee0b05e776cbeb14aed3b49f3775af2a4c5f2b938dcc2b59cbadb89',
    '0xede78b4f1106e022ac7c5af5d0cf0dc9c44d5a329386c071d32e995f1ecb7f9a',
    '0x190981c2ada6c6b20fe9c7aefbf04f3aaa6da47b8e6853a17a8680fb34da156d'
]


prover_thread = [] #list of prover thread
prover_list_account = [] #list of prover account 
prover_addresses = [] # list of provers addresses


contract_creator_deployed = None # contrat deployed, will have to be a list of contracts

rpc, rpc_callbacks = mk_rpc()
#rpc("/stdlib/setProviderByName","TestNet")
rpc("/stdlib/setProviderByEnv",{
    #"ETH_NODE_URI":"https://tiniest-neat-field.matic-testnet.discover.quiknode.pro/6cf11cc8bcbdde3b18c83f183958f440ae58b33f/"
    # "ETH_NODE_URI":"https://sepolia.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e"
    "ETH_NODE_URI":"https://goerli.infura.io/v3/9d7a8c9148c74ee194fd9f5da2ceb98e"
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
        print("USING this Address: ",prover_addresses[i])
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
                
            print("Address used: ",prover_addresses[i],"\n")
            # print("sleeping")
            # time.sleep(15)
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
        '0xC4A9067cE5542899510e6cB8A2Eb84A0a0953eDE',
        '0x63d3e6E0d2E762570819086f3E6dEF5061a27890',

        '0xfbe72863099f8fCAFe6Df5626692013Ce2e83ec3',
        '0x7e90fCc0B6a4459A2c47A2b015c37fB5340aCcb5',
        '0x87985fC3dCE979C09E3c3e745A7A0B464540CA82',
        '0x1fE37BD94109bA874a235B44fA79fC2d7710F1B0',

        '0x7b3180CFeBc06f78Cc55D2bA19cA24dfa2d1fe44',
        '0x9F81B843da3c2d66b08d7Af60c1FE7D79e20771E',
        '0xf71Fea9ED70597c365B5D8A2bD78e04E31654c5e',
        '0x1aF193411dDf746C501459406e8f00f465E11433',

        '0x3AC3A765E4669E0e124C8f1E5104F56a051F7F62',
        '0x605Ef12afC9912fE95A8B9b75b5e9E777AEb7107',
        '0xe61B884f7E7DEa7413c6d65889bC04632241f81d',
        '0x38102a9Abc98EaCAFbd3a92271aB0B9456C3bCdC', 

        '0xA6657AE3cd2444d523408B3453cB4014eE6eA461',
        '0xf3feFd5613A47684A91246e5a9Fb5945983a86c0',
        '0xF13D193A1f808AF9a132C75D40B3934abdeA037e',
        '0x3d424297c1375222C4EafFF32a9aF8bD87eF1C34',

        '0x746ACeB2ceF19957F3d13523C9b030FBF69bdfCf',
        '0x647447d3265bf7F0969eDcef8F4DbeBFB54aaBAC',
        '0x6ea997Cff0e32d634d9a043553Cd465C7E9204D5',
        '0x53c6b740a464C5Ce3825a45AF39f9310381579A9',

        '0x52aD2B5f34a0e61c0D4594BA0524F58Fbd76a30d',
        '0x872c0B06e9FcA7D822c4Ba3F66DE5AdF91bfa7a8',
        '0x844fcEfB192f99997D707fa516EDaFd75868ae49',
        '0x3587C8b93683b268952F4e62A0E0F0c37C791B9F'
    ]

    time_delta_list = []
 
    for (i,t) in enumerate(prover_thread):
        t.join()
        delta = end_list[i]-start_list[i]
        time_delta_list.insert(i, delta)
        print("new delta: ", delta)
        


    for provUser in prover_list_account:
        rpc("/forget/ctc", provUser)

    build_chart(time_delta_list,wallet_pub_key[:PROVER_NUMBER])
    writeResultsDeploy(time_delta_list[:len(LOCATION_LIST_PROV)])
    num_attachers = PROVER_NUMBER-len(LOCATION_LIST_PROV)
    writeResultsAttach(time_delta_list[num_attachers:])
   


def build_chart(time_delta_list,wallet_pub_key):
    # time_delta_list = [4.3,2.3,2.1,1.4]
    # wallet_pub_key = ["Aaaa","adddssf","dssdsds","ggkdk"]
    # plotting the time of deploy and transaction for each account
    height = time_delta_list
    bars = (wallet_pub_key)
    x_pos = np.arange(len(bars))
    colorsList = ['orange'] * len(LOCATION_LIST_PROV)
    n_attachers = PROVER_NUMBER-len(LOCATION_LIST_PROV)
    for i in range(n_attachers):
        colorsList.append('#7eb54e')
    color_legend = {'Deploy':'orange', 'Attach':'#7eb54e'}         
    labels = list(color_legend.keys())
    handles = [plt.Rectangle((0,0),1,1, color=color_legend[label]) for label in labels]
    assert(len(colorsList) ==  PROVER_NUMBER)
    plt.legend(handles, labels)
    plt.bar(x_pos, height, color= colorsList)
    plt.xticks(x_pos, bars, rotation=90)
    plt.xlabel('Accounts')
    plt.ylabel('Seconds')  

    # Create names on the x-axis
    plt.xticks(x_pos, bars)

    # Show graphic
    #plt.show()

    plt.savefig('./outputPerformance.png')
    
def writeResultsDeploy(time_delta_list):
    meanList = round(np.mean(time_delta_list),2)
    max_val = round(np.max(time_delta_list),2)
    min_val = round(np.min(time_delta_list),2)
    devStd = round(np.std(time_delta_list),2)
    variance = round(np.var(time_delta_list),2)
    f = open("resultsDeploy.txt", "w")
    f.write("Deploy Performances")
    f.write("mean: "+str(meanList)+"\n")
    f.write("max: "+str(max_val)+"\n")
    f.write("min: "+str(min_val)+"\n")
    f.write("dev standard: "+str(devStd)+"\n")
    f.write("variance: "+str(variance)+"\n")
    f.close()

def writeResultsAttach(time_delta_list):
    meanList = round(np.mean(time_delta_list),2)
    max_val = round(np.max(time_delta_list),2)
    min_val = round(np.min(time_delta_list),2)
    devStd = round(np.std(time_delta_list),2)
    variance = round(np.var(time_delta_list),2)
    f = open("resultAttach.txt", "w")
    f.write("Attach Performances")
    f.write("mean: "+str(meanList)+"\n")
    f.write("max: "+str(max_val)+"\n")
    f.write("min: "+str(min_val)+"\n")
    f.write("dev standard: "+str(devStd)+"\n")
    f.write("variance: "+str(variance)+"\n")
    f.close()

def main():
    startSimulation()
    # generateOLC(11.3986586,44.4864416) # san lazzaro municipio
    # generateOLC(11.3501333,44.4970137) # piazza scaravilli
    
    
if __name__ == '__main__':
    main()




