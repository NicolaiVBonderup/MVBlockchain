# The SHA256 hashing function we'll be using for Proof of Work
from hashlib import sha256
import transaction
import time

class Block:

    def __init__(self, *args):
        self.transactions = []
        self.timestamp = None
        self.prev_hash = None
        self.hash = None
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

        
class InvalidBlock(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)