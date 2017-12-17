class Phonebook:
    
    def __init__(self):
        self.nodes = []

    def add_peer_to_phonebook(self, peer):
        # UID, Port, Public Key
        self.nodes.append(peer)
