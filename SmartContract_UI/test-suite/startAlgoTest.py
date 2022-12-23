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
import concurrent.futures
import random
from scipy.stats import t
'''
    ---------------------------------------------------------------------------------------
    ------------------    THIS SCRIPT MUST BE RUN ON ALGORAND TESTNET    ------------------
    ---------------------------------------------------------------------------------------
'''
SMART_CONTRACT_MAX_USER = 3 # this is the same variable of index.rsh. They must be equals!

# ❗️ Every location must contains 4 provers which corresponds to (SMART_CONTRACT_MAX_USER + 1) users
LOCATION_LIST_PROV = ["7H369F4W+Q8", "7H369F4W+Q9", "7H368FRV+FM", "7H368FWV+X6", "7H367FWH+9J", "7H368F5R+4V", "7H369FXP+FH", "7H369F2W+3R"] # list of Provers locatios. Used for build the prover object
PROVER_NUMBER = 32 # number of provers for the entire system

assert(PROVER_NUMBER/len(LOCATION_LIST_PROV) == 4) #There must be (SMART_CONTRACT_MAX_USER+1) users for each location. So increase the number of locations in LOCATION_LIST_PROV, or decrease the PROVER_NUMBER

DID_list = [] #Contain the list of DID already generated (generated with a random process). Will be filled at runtime
 #The Key is the location; the Value is an array (contains all the DID in that location). Will be filled at runtime

'''
    This method will generate n° prover objects setting their attribute such as DID, location or the consensus network account.
    The DID created will be unique.
    This method will create mapping_list_did dictionary, which will be used to check the users nearby.
'''
def generateProvers(n_users_to_generate, list_loc,mapping_list_did):
    proversObjectList = []

    count = 0
    for i in range(n_users_to_generate):
        #use to assign each ID to the location
        if count == len(list_loc):
            count = 0

        # choose the location from the list of locations
        chooseLocation = list_loc[count] #there are SMART_CONTRACT_MAX_USER + 1 elements for each location
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
            proofs_received_array=[],
            title_report="Report Title here ...",
            description_report="Descrition of the report ...",
            tx_id_data="None")
        
        #update some attributes of the prover objects
        account_prov = prov.createAccount(i) #passing the number of prover to create
        prover_list_account.append(account_prov)
        prov.account = account_prov

        prover_addresses.append(format_address(account_prov))

        proversObjectList.append(prov)

        count += 1

    return proversObjectList



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
    'wide theme range pulse husband clever cruel kid double right choice match ill bless garlic flash zoo around ability creek exist armed hand able service', # JI7VRGDIANFNABPJL6PWVGCP42NZGQVV7T3QVJD6P47EKQP2BXSFMPU7RA

    'ethics candy explain paddle broccoli violin uncle merit jealous snack turkey trust alley spike champion boost artwork liberty brass monkey cereal strategy used abstract afraid', # 7QO73MI5LUZH4GJNXKUAYY2RFSB35IAY4ERSJAZAYZZRG3MYLW3BBXRQ4E
    'second around tag early favorite embody apple pitch love wide auction only puzzle essence judge baby random match shallow boy crop gate table absent theme', # HPNXA2SB3RM22SV2QL3LI6YGOQZ6RQCAG6ANZ27DL657EOFWTRJKFGOTN4
    'soul copy country island suffer soap bunker salt please theme glance harvest inflict citizen nut biology hood never banner gold donate feature nothing ability exclude', # ITJVBY6NAGIHNHUB2YUYATZZK5BSDDNSV43MZA7F675GO3QROB27UMRY44
    'piece list portion scare reveal bottom bar tomorrow gossip age silver case tone wing march emotion exact card sword skull budget estate grace above million', # KYRUST4GUA4ZWSSXD6XS27IYMUTGRGQE4VRZNK3I77KFQLHFZI2VXUKPMA
    
    'play drum afford elite promote refuse random twelve bright icon prosper chief boost cannon carbon monkey attack end better reward merit ride fit abandon find', # NCPVP7WVVZ6MKILOYQASO2AM26JIWVWSWJN4UTI3QBJBCKMZHGFMG7AG54
    'rhythm pole visual cart judge focus fiscal accident blame crouch aspect shiver refuse morning course midnight salmon toast rain desert imitate portion negative above glare', # WIXIIBVJIZTDKYDVLDATSWEHOOBQ27QHJEO2E76Q4YZ35E42L5FCE2G3L4
    'plate build physical type cruise bench sauce portion face dress dentist effort canyon faith tiger load flock polar cup merit push sister earth abstract taste', # HEWT2HVPM4GKUBBSOV4BSY3URKYYGLICPSSU4H43DWCSWCO3CXQT2IQPDY
    'dutch assist faith scare modify equip detail exotic flee chronic journey session flight clarify able misery make mountain entry easily clap sign lock abandon taxi', # R3Z7QT5YLA2QISYKQOGQYDK7RHRKDSAVWS7IGXZNHERJ5GGIORFK7C6IYQ

    'solution school lyrics mass hurt miracle family culture tourist sing wheel raven recycle question air devote inflict snack woman energy swing chapter plug ability mandate', # 2USVA6CFEPHG2TBNFK5A3GL6WLMOMET5SW6A57YVQ2JGBRB7YVMP4XFSXA
    'crisp this install text salon early turtle foster bid weapon large about tomato inflict cupboard raven fire resist veteran hill inspire chat panel absorb jungle', # NOQ6ZM3RPEOFXVA5K4VOO5BLEOT5KUYENNM6GZD3FLUH7O7DPBWGFALXAM
    'exchange veteran axis clap close brief merge shuffle tide birth draw width warrior caution crime tide adult invest orphan stage film horn spring absorb armor', # NP5OQPDB4OPEAV3UXSGEPWM7CMATFXXXA7436QD2DVSRGJCIMN3GMHTG7E
    'drill marriage peasant exchange adult panic blast differ manual endless output silver else midnight winter clay fancy treat flat spy blanket lyrics afford absent glass', # 5XWP6SGUKE4KEJZZ76T35FQX5W7EN6YGPUCGZDULVOW4K3KNNFBSCOB3KI
    'glass beauty armed flip museum hospital trash provide season humble number unhappy south beauty tail basket marriage sing conduct card festival unaware tattoo absorb order', # LMGA7YRP4B4QR3YMWPNGCOSWCMUMTF5FSIT5SSY2POIZSH7GKVHKCW6MFI
    'world mutual foster husband gown minor mansion trigger stuff today palace dust retire bachelor sword spare stock usage split insect fence sauce club about dizzy', # KHF6VRW626XJITAZ32L2BEO5PTF77PDHJ46Y255U6ARPRMF6JPEHBUEPTY
    'unfold tattoo above truly excuse connect napkin crouch fancy scheme ensure because pact always era airport make deposit salon canal debris section paper abstract cloth', # CB2N75VJMES3UFPRW5WQV4KHZYUADLIHJQ34Y4R532MVXB72AAXOHVPFKE
    'sister medal before gather nose globe twenty sand office surge more exact elegant inside crucial valid only frozen law gravity uniform ankle melt able follow' # ED45XUALM6FOEIOPFVU2G7CFPZ6GHYZ22ELJSDDONIDVERHJ2E4TNYLPGA

]


prover_thread = [] #list of prover thread
prover_list_account = [] #list of prover account 
prover_addresses = [] # list of provers addresses

contract_creator_deployed = None # contrat deployed, will have to be a list of contracts

rpc, rpc_callbacks = mk_rpc()
rpc("/stdlib/setProviderByName","TestNet")

print("\t\t The consesus network is: ", rpc('/stdlib/connector'))
#STARTING_BALANCE = rpc("/stdlib/parseCurrency", 1500) 


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
        #print("Inserting Creator's information into the contract ...")
        creatorThread = Thread(target=play_Creator, args=(ctc_creator, proverObject.location, proverObject.did, 'proof', proverObject.tx_id_data))
       
        return creatorThread, ctc_creator

    # this method will interact with index.py
    def attachToSmartContract(self, proverAttacherObject, ctc_creator):
        #print("Calling play bob")
        attacherThread = Thread(target=play_bob, args=(ctc_creator, proverAttacherObject.account, proverAttacherObject.location, proverAttacherObject.did, 'proof', proverAttacherObject.tx_id_data))
        #attacherThread.start()
        #print("playbob called successfully")
        return attacherThread



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
    
    e.g.: generateOLC(11.3474453,44.4930181 )
'''
def generateOLC(latitude, longitude):
    location_encoded = olc.encode(latitude, longitude) #lat - long - N° digits. Default is 10 digits which allow 14m of precisions
    print('Encoded location: ', location_encoded)
    return location_encoded


# START the simulation
def startSimulation(num_p, list_loc,mapping_list_did):
    #generate N random provers
    generate_prover_list = generateProvers(num_p, list_loc,mapping_list_did) # try with 8, 12, 16 etc.

    initial_test = 0

    print("\n\n----------- START -----------")
    dict_location_sc = {} # keep track if the smart contract is already associated to this particular location. Its lenght will be equal to NUMBER_OF_LOCATIONS

    # Starting prover steps
    for i in range(0, num_p): #for every prover of the entire system ...
        prov = generate_prover_list[i]

        # Find neighbours
        neighbours = prov.find_neighbours(prov.location, mapping_list_did)
        if neighbours: 

            print('→ 🪪 Prover DID: ', prov.did,'\n 📍 Location: ', prov.location, '\n    Neighbours: ', neighbours,'\n',)

            # the IF will simulate the initial check inside the hypercube. If the SC is not associated to a location in the hypercube (the dictionary in this case) then deploy a new smart contract and insert its ID and location inside the hypercube
            if (prov.location in dict_location_sc) == False: # if the location is not inserted inside the dict that track the SC deployed, then deploy a new smart contract and add the contract address to the dict 
                #print(" Deploying the smart contract ...")
                creatorThread, contract_creator_deployed = prov.deploySmartContract(prov)
                creatorThread.start()
                prover_thread.append(creatorThread)

                dict_location_sc[prov.location] = contract_creator_deployed #insert the contract_id inside the dict_location_sc which track the contract deployed
            else:
                print("ELABORATING USER WITH DID: ",prov.did)
                if initial_test == 0:
                    print("Waiting some time...")
                    time.sleep(0)
                    initial_test = 1
                retrieved_ctc = dict_location_sc[prov.location]
                proverThread = prov.attachToSmartContract(prov, retrieved_ctc)

                proverThread.start()
                prover_thread.append(proverThread)


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

        "7QO73MI5LUZH4GJNXKUAYY2RFSB35IAY4ERSJAZAYZZRG3MYLW3BBXRQ4E",
        "HPNXA2SB3RM22SV2QL3LI6YGOQZ6RQCAG6ANZ27DL657EOFWTRJKFGOTN4",
        "ITJVBY6NAGIHNHUB2YUYATZZK5BSDDNSV43MZA7F675GO3QROB27UMRY44",
        "KYRUST4GUA4ZWSSXD6XS27IYMUTGRGQE4VRZNK3I77KFQLHFZI2VXUKPMA",

        "NCPVP7WVVZ6MKILOYQASO2AM26JIWVWSWJN4UTI3QBJBCKMZHGFMG7AG54",
        "WIXIIBVJIZTDKYDVLDATSWEHOOBQ27QHJEO2E76Q4YZ35E42L5FCE2G3L4",
        "HEWT2HVPM4GKUBBSOV4BSY3URKYYGLICPSSU4H43DWCSWCO3CXQT2IQPDY",
        "R3Z7QT5YLA2QISYKQOGQYDK7RHRKDSAVWS7IGXZNHERJ5GGIORFK7C6IYQ",


        "2USVA6CFEPHG2TBNFK5A3GL6WLMOMET5SW6A57YVQ2JGBRB7YVMP4XFSXA",
        "NOQ6ZM3RPEOFXVA5K4VOO5BLEOT5KUYENNM6GZD3FLUH7O7DPBWGFALXAM",
        "NP5OQPDB4OPEAV3UXSGEPWM7CMATFXXXA7436QD2DVSRGJCIMN3GMHTG7E",
        "5XWP6SGUKE4KEJZZ76T35FQX5W7EN6YGPUCGZDULVOW4K3KNNFBSCOB3KI",

        "LMGA7YRP4B4QR3YMWPNGCOSWCMUMTF5FSIT5SSY2POIZSH7GKVHKCW6MFI",
        "KHF6VRW626XJITAZ32L2BEO5PTF77PDHJ46Y255U6ARPRMF6JPEHBUEPTY",
        "CB2N75VJMES3UFPRW5WQV4KHZYUADLIHJQ34Y4R532MVXB72AAXOHVPFKE",
        "ED45XUALM6FOEIOPFVU2G7CFPZ6GHYZ22ELJSDDONIDVERHJ2E4TNYLPGA"
    ]

    time_delta_list = []
 
    for (i,t) in enumerate(prover_thread):
        t.join()
        delta = end_list[i]-start_list[i]
        time_delta_list.insert(i, delta)
        print("new delta: ", delta)
   

    for provUser in prover_list_account:
        rpc("/forget/ctc", provUser)

    
    num_attachers = num_p - len(list_loc)
    times_deploy = time_delta_list[0:len(list_loc)]
    print("time_delta_list: ", time_delta_list)
    print("times_deploy: ", times_deploy)
    times_attach = time_delta_list[len(list_loc):num_p]
    print("times_attach: ", times_attach)

    print("\nlista totale di times: ", len(time_delta_list))
    print("list di deploy times: ", len(times_deploy))
    print("lista di attach times: ", len(times_attach))
    print("\nlista di wallet pub key deployer: ", len(wallet_pub_key[0:len(list_loc)]))
    print("\n lista di wallet pub key attacher: ", len(wallet_pub_key[len(list_loc):num_p]))

    
    build_chart(times_deploy, wallet_pub_key[0:len(list_loc)],"deploy", num_p, list_loc)
    f = open("time_delta_list_deploy_algo.txt", "w")
    deployTimes_list1 = str(times_deploy) + "\n"
    f.write(deployTimes_list1)
    
    build_chart(times_attach, wallet_pub_key[len(list_loc):num_p], "attach", num_p, list_loc)

    f = open("time_delta_list_attach_algo.txt", "w")
    deployTimes_list2 = str(time_delta_list[len(list_loc):num_p]) + "\n"
    f.write(deployTimes_list2)

    #build_chart(time_delta_list,wallet_pub_key[len(list_loc):num_p],"deploy_attach", num_p, list_loc)
    writeResultsDeploy(times_deploy,"algo")
    writeResultsAttach(times_attach,"algo")


    return times_deploy, times_attach, time_delta_list


def build_chart(time_delta_list,wallet_pub_key,nameChart, num_p, list_loc):
    # time_delta_list = [4.3,2.3,2.1,1.4]
    # wallet_pub_key = ["Aaaa","adddssf","dssdsds","ggkdk"]
    # plotting the time of deploy and transaction for each account
    legend = False
    if nameChart == 'attach' or nameChart == 'deploy':
        legend = False # I don't want the legend
    else:
        legend = True
    height = 0
    height = time_delta_list
    
    bars = (wallet_pub_key)
    x_pos = np.arange(len(bars))
    
    if legend:
        colorsList = ['orange'] * len(list_loc)
        n_attachers = num_p-len(list_loc)
        for i in range(n_attachers):
            colorsList.append('#7eb54e')
        color_legend = {'Deploy':'orange', 'Attach':'#7eb54e'}         
        labels = list(color_legend.keys())
        handles = [plt.Rectangle((0,0),1,1, color=color_legend[label]) for label in labels]
        assert(len(colorsList) ==  num_p)
        plt.legend(handles, labels)
        plt.bar(x_pos, height, color= colorsList)
    else:
        plt.bar(x_pos, height, color='orange')
    plt.xticks(x_pos, bars, rotation=90)
    plt.xlabel('Accounts')
    plt.ylabel('Seconds')  

    # Create names on the x-axis
    #plt.xticks(x_pos, bars)

    # Show graphic
    #plt.show()

    plt.savefig('./outputPerformanceAlgo_'+nameChart+'.png')
    plt.figure()
    
def writeResultsDeploy(time_delta_list, name):
    meanList = round(np.mean(time_delta_list),2)
    max_val = round(np.max(time_delta_list),2)
    min_val = round(np.min(time_delta_list),2)
    devStd = round(np.std(time_delta_list),2)
    variance = round(np.var(time_delta_list),2)

    dof = len(time_delta_list)-1 
    confidence = 0.95
    t_crit = np.abs(t.ppf((1-confidence)/2,dof))
    print(meanList-devStd*t_crit/np.sqrt(len(time_delta_list)), meanList+devStd*t_crit/np.sqrt(len(time_delta_list))) 


    f = open("resultsDeploy_"+name+".txt", "w")
    f.write("Deploy Performances")
    f.write("mean: "+str(meanList)+"\n")
    f.write("max: "+str(max_val)+"\n")
    f.write("min: "+str(min_val)+"\n")
    f.write("dev standard: "+str(devStd)+"\n")
    f.write("variance: "+str(variance)+"\n")
    f.close()

def writeResultsAttach(time_delta_list, name):
    meanList = round(np.mean(time_delta_list),2)
    max_val = round(np.max(time_delta_list),2)
    min_val = round(np.min(time_delta_list),2)
    devStd = round(np.std(time_delta_list),2)
    variance = round(np.var(time_delta_list),2)

    dof = len(time_delta_list)-1 
    confidence = 0.95
    t_crit = np.abs(t.ppf((1-confidence)/2,dof))
    print(meanList-devStd*t_crit/np.sqrt(len(time_delta_list)), meanList+devStd*t_crit/np.sqrt(len(time_delta_list))) 

    f = open("resultAttach_"+name+".txt", "w")
    f.write("Attach Performances")
    f.write("mean: "+str(meanList)+"\n")
    f.write("max: "+str(max_val)+"\n")
    f.write("min: "+str(min_val)+"\n")
    f.write("dev standard: "+str(devStd)+"\n")
    f.write("variance: "+str(variance)+"\n")
    f.close()
            
def main():
    number_provers = [8, 16, 24, 32]
    
    list_locations = [
                ["7H369F4W+Q8", "7H369F4W+Q9"],
                ["7H369F4W+Q8", "7H369F4W+Q9", "7H368FRV+FM", "7H368FWV+X6"],
                ["7H369F4W+Q8", "7H369F4W+Q9", "7H368FRV+FM", "7H368FWV+X6", "7H367FWH+9J", "7H368F5R+4V"],
                ["7H369F4W+Q8", "7H369F4W+Q9", "7H368FRV+FM", "7H368FWV+X6", "7H367FWH+9J", "7H368F5R+4V", "7H369FXP+FH", "7H369F2W+3R"]
            ]
    mean_list_deploy = []
    mean_list_attach = []
    for num_p in range(0,len(number_provers)):
        mapping_list_did = {}
        deploy_times = []
        attach_times = []
        time_delta_list = []
        deploy_times, attach_times, time_delta_list = startSimulation(number_provers[num_p], list_locations[num_p],mapping_list_did)
        mean_deploy_times = np.mean(deploy_times)
        mean_attach_times = np.mean(attach_times)
        mean_list_deploy.append(mean_deploy_times)
        mean_list_attach.append(mean_attach_times)

    # ---------- PLOT LINES ----------
    f = open("ValoriPerPlot_Algo_Line.txt", "w")
    valoriDaPlottareLineD = "\nDEPLOY LINE PLOT: " + str(number_provers) +"  -  "+ str(mean_list_deploy) +"\n"
    valoriDaPlottareLineA = "ATTACH LINE PLOT: " + str(number_provers) +"  -  "+ str(mean_list_attach) +"\n"
    
    f.write(str(time_delta_list))
    f.write(valoriDaPlottareLineD)
    f.write(valoriDaPlottareLineA)
    # plt.plot(number_provers, mean_list, label = "Algorand")
    # plt.legend()
    # plt.show()
    # ---------- END LINES ----------



if __name__ == '__main__':
    main()

