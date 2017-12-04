# The SHA256 hashing function we'll be using for Proof of Work
from hashlib import sha256
import transaction
import time
import uuid

class Block:

    def __init__(self, *args):
        self.uid = uuid.uuid4().hex
        self.transactions = []
        self.timestamp = None
        self.prev_hash = None
        self.hash = None
        self.nonce = None
        # Adds a list of transactions if given in the constructor.
        if args:
            for arg in args:
                self.add_transaction(arg)

    def hash_block(self):
        hash = sha256(bytearray(str(self.prev_hash) + str(self.timestamp) + self.transactions[-1].hash, "utf-8")).hexdigest()
    
        return hash

    def add_transaction(self, transac):
        # Links the new transaction to the previous transaction, if there is one.
        if len(self.transactions) > 0:
            transac.link(self.transactions[-1])
        # Hashes the transaction together with the hash of the previous transaction to create integrity in the block.
        transac.seal()
        # Ensures there's not an invalid transaction in the block.
        transac.validate()
        self.transactions.append(transac)

    # The block hash only needs to incorporate the head message hash, which then transitively includes all prior hashes.
    def link(self, block):
        self.prev_hash = block.hash
        
    def seal(self):
        self.timestamp = time.time()
        self.hash = self.hash_block()

    def validate(self):
        for i, transac in enumerate(self.transactions):
            transac.validate()
            # Throws an error if a transaction's previous hash does not match the hash of the transaction behind it in the block.
            if i > 0 and transac.prev_hash != self.transactions[i-1].hash:
                raise InvalidBlock("Invalid block: Message #{} has invalid message link in block: {}".format(i, str(self)))
                
    def hash_with_nonce(self, nonce=None):
        nonce = nonce or self.nonce

        message = sha256()
        message.update(str(self.uid).encode('utf-8'))
        message.update(str(nonce).encode('utf-8'))
        message.update(str(self.transactions).encode('utf-8'))
        message.update(str(self.prev_hash).encode('utf-8'))

        return message.hexdigest()
        
    def has_enough_transactions(self):
        if len(self.transactions) >= 4:
            return True

    def validate_hash(self, attempted_hash):
        return attempted_hash.startswith('0000')

    @property
    def mined(self):
        return self.nonce is not None

    def mine(self):
        # If a nonce is not already set, and the block isn't mined, we just start from 0.
        mining_nonce = self.nonce or 0

        while True:
            attempted_hash = self.hash_with_nonce(nonce=mining_nonce)
            if self.validate_hash(attempted_hash):
                print ("Mining complete. Nonce: " + str(mining_nonce) + " - Hash: " + str(attempted_hash))
                self.nonce = mining_nonce
                return
            else:
                mining_nonce += 1

        
class InvalidBlock(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)