import ipfshttpclient

from src.config import SUPERSET_THRESHOLD
from src.utils import *
from algorand_scripts.write_on_blockchain import *


DOWNLOAD_FOLDER = './objects'


class Client:
    def __init__(self, addr, server):
        self.ipfs = ipfshttpclient.connect(addr)
        self.id = self.ipfs.id()['ID']
        self.server = server
        #self.algorand_wallet = algorand_wallet
        log(self.id, 'CONNECTION', '{}'.format(addr))

    def add_obj(self, path, keyword, algorand_wallet):
        ##########################################
        # insert in ipfs and Algorand blockchain #
        ##########################################
        obj_hash = self.ipfs.add(path)['Hash']
        transactionID = make_transaction(algorand_wallet, obj_hash)


        if request(create_binary_id(self.server), INSERT, {'keyword': str(keyword), 'obj': transactionID, 'hop': str(0)}).text == 'success':
            res = 'REFERENCE ({},{}) ADDED'.format(keyword, transactionID) #inserting the transaction ID in DHT
            log(self.id, INSERT[1:], res)
        else:
            res = 'REFERENCE ({},{}) ALREADY EXIST'.format(keyword, transactionID)
            log(self.id, INSERT[1:], res)
        return res

    #TODO: understand if client CAN remove from DHT. Can client remove the Transaction ID ?
    def remove_obj(self, tx_id, keyword):
        if request(create_binary_id(self.server), REMOVE, {'keyword': str(keyword), 'obj': client}).text == 'success':
            res = 'REFERENCE ({},{}) REMOVED'.format(keyword, client)
            log(self.id, REMOVE[1:], res)
        else:
            res = 'REFERENCE ({},{}) NOT EXIST'.format(keyword, client)
            log(self.id, REMOVE[1:], res)
        return res

    #getting IPFS hash from blockchain, inserting the tx_id and check if exists in DHT
    '''
        User insert a specific transaction ID, then this function will download the IPFS hash written inside the note field
    '''
    def get_obj(self, obj):
        try:
            self.ipfs.get(obj, target=DOWNLOAD_FOLDER)
            res = "OBJECT '{}' DOWNLOADED".format(obj)
            log(self.id, 'GET', res)
        except Exception:
            res = "OBJECT '{}' NOT FOUND".format(obj)
            log(self.id, 'GET', res)
        return res

    def pin_search(self, keyword, threshold=-1):
        if threshold == -1:
            res = get_response(request(create_binary_id(self.server), PIN_SEARCH, {'keyword': str(keyword)}).text)
        else:
            res = get_response(request(create_binary_id(self.server), PIN_SEARCH, {'keyword': str(keyword), 'threshold': threshold}).text)
        if len(res) > 0:
            log(self.id, PIN_SEARCH[1:], '{}'.format(res))
        else:
            res = []
            log(self.id, PIN_SEARCH[1:], 'NO RESULTS FOUND')
        return res

    def superset_search(self, keyword, threshold=SUPERSET_THRESHOLD):
        res = get_response(request(create_binary_id(self.server), SUPERSET_SEARCH, {'keyword': str(keyword), 'threshold': threshold, 'sender': 'user'}).text)
        if len(res) > 0:
            log(self.id, SUPERSET_SEARCH[1:], '{}'.format(res))
        else:
            res = []
            log(self.id, SUPERSET_SEARCH[1:], 'NO RESULTS FOUND')
        return res

    def close(self):
        self.ipfs.close()
        return
