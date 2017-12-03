import transaction
import block

class Blockchain:
    
    def __init__(self):
        self.blocks = []

    def add_block_to_ledger(self, block):
        # Adding the hash of the previous block in your ledger to the block we just received.
        if len(self.blocks) is not 0:
            block.prev_hash = self.blocks[-1].hash
        # Hashes the block together with the hash of the previous block to create integrity in the chain.
        block.seal()
        # Ensures there's not an invalid block in the chain.
        block.validate()
        self.blocks.append(block)
        
    # Makes sure the chain has no tampered blocks
    def validate(self):
        for block in self.blocks:
            try:
                block.validate()
            except InvalidBlock as ex:
                raise InvalidBlockchain("Invalid blockchain at block {} caused by: {}".format(i, str(ex)))

                
class InvalidBlockchain(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)