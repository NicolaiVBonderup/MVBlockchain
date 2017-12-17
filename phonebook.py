class Phonebook:
    
    def __init__(self):
        self.nodes = {}
        self.clients = {}

    def add_peer_to_phonebook(self, UID, peer):
        # UID, port, pubkey
        self.nodes.update({UID: peer})
        
    def add_client_to_phonebook(self, name, key):
        self.clients.update({name : key})

    def get_peer_by_UID(self, name):
        return self.nodes.get(name)
        
    def get_all_peers_for_announcement(self):
        peer_list = []
        
        for idx, uid in enumerate(self.nodes):
            dict = self.nodes.get(uid)
            peer_list.append(dict.get('port'))
    
        return peer_list
        
    def get_all_peers(self):
        peer_list = []
        
        
        for uid, dict in enumerate(self.nodes):
            peer_list.append((dict.get('port'), dict.get('pubkey')))
    
        return peer_list