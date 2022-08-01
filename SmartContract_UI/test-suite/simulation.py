from openlocationcode import openlocationcode as olc

WITNESS_NUMBER = 1
PROVER_NUMBER = 1

class Witness:
    def __init__(self, did, public_key, private_key, proofs_array_computed, location):
        self.did = did
        self.public_key = public_key
        self.private_key = private_key
        self.proofs_array_computed = proofs_array_computed
        self.location = location
    
    def verify_location_Prover(self, locationProver):
        # send proof
        pass
    
    '''
        This method allow to the witness to compute the distance from the prover.

        In the real case we'll use the bluetooth range, so this function might not exists.
    '''
    def computed_distance_from_prover(self, locationWitnes, locationProver):
        pass




class Prover(Witness):
    def __init__(self, did, public_key, private_key, proofs_array_computed, location, proofs_received_array):
        super().__init__(did, public_key, private_key, proofs_array_computed, location)
        self.proofs_received_array = proofs_received_array

    def send_location(self):
        # return proof
        pass

    '''
        This method allow to the prover to compute the distance from the witness.

        In the real case we'll use the bluetooth range, so this function might not exists.
    '''
    def computed_distance_from_witness(self, locationWitnes, locationProver):
        super(Prover, self).computed_distance_from_prover(locationWitnes, locationProver)
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


def createWitness(did, public_key, private_key, proofs_array_computed, location):
    wit = Witness(
        did= did,
        public_key= public_key,
        private_key= private_key,
        proofs_array_computed= proofs_array_computed,
        location= location)

    return wit

def createProver(did, public_key, private_key, proofs_array_computed, location, proofs_received_array):
    prov = Prover(
        did= did, public_key= public_key,
        private_key= private_key,
        proofs_array_computed= proofs_array_computed,
        location= location,
        proofs_received_array= proofs_received_array)
    
    return prov

def generateOLC(latitude, longitude):
    location_encoded = olc.encode(latitude, longitude) #lat - long - N° digits. Default is 10 digits which allow 14m of precisions
    print('Encoded location: ', location_encoded)
    return location_encoded

def startSimulation():
    #generateOLC

    # for i in WITNESS_NUMBER
    wit = createWitness(  
        did= "0",
        public_key= "SHJDAJAKRHAKD",
        private_key= "xxxxx",
        proofs_array_computed= [],
        location= "7H368FJQ+84")


    # for i in PROVER_NUMBER
    prov = createProver(
        did= "1",
        public_key= "FFFFFFFFF",
        private_key= "xxxxxxx",
        proofs_array_computed= [],
        location= "7H369FXP+FH",
        proofs_received_array=[])
    
    print('wit ', wit.did)
    print('prov ', prov.did)

    # Move the Prover

    print(olc.isValid(prov.location))









if __name__ == '__main__':
    startSimulation()