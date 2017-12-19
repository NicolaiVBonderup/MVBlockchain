from rsa import PublicKey

class Phonebook:
    
    def __init__(self):
        self.nodes = {}
        self.clients = {}

    def add_peer_to_phonebook(self, UID, peer):
        # UID, port, pubkey_e, pubkey_n
        self.nodes.update({UID: peer})
        
    def update_phonebook(self, client_dict, node_dict):
        
        for idx, key in enumerate(client_dict):
            if key not in self.clients:
                val = client_dict.get(key)
                self.clients.update({key:val})
                
        for idx, key in enumerate(node_dict):
            if key not in self.nodes:
                val = node_dict.get(key)
                self.nodes.update({key:val})
                
        
        
    def add_client_to_phonebook(self, name, key):
        # uid, pubkey_e, pubkey_n
        self.clients.update({name : key})

    def get_peer_by_UID(self, name):
        return self.nodes.get(name)
        
    def get_pubkey_from_UID(self, name):
        client_dict = self.clients.get(name)
        pubkey_e = client_dict.get('pubkey_e')
        pubkey_n = client_dict.get('pubkey_n')
        client_pubkey = PublicKey(pubkey_n, pubkey_e)
        return client_pubkey
        
    def get_all_peers_for_announcement(self):
        peer_list = []
        
        for idx, uid in enumerate(self.nodes):
            dict = self.nodes.get(uid)
            peer_list.append(dict.get('port'))
    
        return peer_list
        
    def get_all_peers(self):
        return (self.nodes, self.clients)