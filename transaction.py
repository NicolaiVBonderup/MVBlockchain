# The SHA256 hashing function we'll be using for Proof of Work
from hashlib import sha256
import time
import transaction as ts

class Transaction:

    def __init__(self, sender, receiver, data):
        self.hash = None
        self.prev_hash = None
        self.timestamp = time.time()
        self.sender = sender
        self.receiver = receiver
        self.data = data
        self.standalone_hash = self.create_standalone_hash()

        # Creates a full hash for the message when it's first received.
    def create_standalone_hash(self):
        return sha256(bytearray(str(self.timestamp) + str(self.data) + str(self.sender) + str(self.receiver), "utf-8")).hexdigest()

        # Hashes the transaction with the preceding transaction, to allow us to tell if preceding hashes have been changed in any way.
    def hash_transaction(self):
        return sha256(bytearray(str(self.prev_hash) + self.standalone_hash, "utf-8")).hexdigest()

        # Links this transaction with a preceding transaction.
    def link(self, msg):
        self.prev_hash = msg.hash
        return self

        # Hashes the current transaction with a combination of its own hash, and a preceding transactions hash.
        # Doing this allows us to tell if any link in the block has been tampered with.
    def seal(self):
        self.hash = self.hash_transaction()
        return self

    def validate(self):
        if self.standalone_hash != self.create_standalone_hash():
            raise InvalidMessage("Invalid standalone hash in message: " + str(self))
        if self.hash != self.hash_transaction():
            raise InvalidMessage("Invalid message hash in message: " + str(self))

class InvalidMessage(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
