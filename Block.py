import json
import time
import sha512

class Block:
    def __init__(self, i, transaction, ts, previousHash):
        self.index = i
        self.transaction = transaction
        self.timestamp = ts
        self.previousHash = previousHash

    def compute_hash(self):
        jblock = json.dumps(self.__dict__, sort_keys=True)
        return sha512.SHA512(jblock)

class BlockChain:
    # Number of leading 0s required in hash
    # Increasing increases the difficulty of the PoW
    leading0s = 2

    def __init__(self):
        self.transactions_offChain = []
        self.chain = []
        self.create_genesis()

    def create_genesis(self):
        Gen = Block(0, [], time.time(), "0")
        Gen.hash = Gen.compute_hash()
        self.chain.append(Gen)

    def PoW(self, block):
        block.num = 0
        bhash = block.compute_hash()
        while not bhash.startswith(0* self.leading0s):
            block.num += 1
            bhash = block.compute_hash()
        return bhash

    def addBlock(self, block, proof):
        # Validate the new block and the chain
        # Check that the previous hash matches
        previous_hash = self.last_block.hash
        if previous_hash != block.previousHash:
            return False
        if not BlockChain.validateBlock(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def validateBlock(self, block, proof):
        # Determine if the hash of the block matches the difficulty
        # Check if the block has been tampered
        if block.hash == block.compute_hash() and block.hash.startswith(0 * self.leading0s):
            return True
        raise ValueError("INVALID BLOCK ADD ATTEMPT (validation)")

    def mine(self):
        if not self.transactions_offChain:
            return False

        block = Block(self.last_block.index, self.transactions_offChain, time.time(), self.last_block.hash)
        proof = self.PoW(block)
        self.addBlock(block, proof)
        self.transactions_offChain = []
        return block.index

    def add_transaction(self, transaction):
        self.transactions_offChain.append(transaction)

    @property
    def last_block(self):
        return self.chain[-1]


if __name__ == "__main__":
    chain1 = BlockChain()

