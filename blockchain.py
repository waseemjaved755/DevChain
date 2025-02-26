import hashlib
import json
from time import time
from uuid import uuid4
from typing import List


class DevChain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof: int, previous_hash: str = None):
        
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        })

        return self.last_block["index"] + 1

    @staticmethod
    def hash(block: dict) -> str:
        
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> dict:
        
        return self.chain[-1]

    def proof_of_work(self, last_block: dict) -> int:
        
        last_proof = last_block["proof"]
        last_hash = self.hash(last_block)

        proof = 0
        while not self.valid_proof(last_proof, proof, last_hash):
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int, last_hash: str) -> bool:
        
        guess = f"{last_proof}{proof}{last_hash}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
