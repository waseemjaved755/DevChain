from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from blockchain import DevChain

app = FastAPI()


blockchain = DevChain()


node_identifier = str(uuid4()).replace("-", "")


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float


@app.get("/mine")
def mine():
    
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    return {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }


@app.post("/transactions/new")
def new_transaction(transaction: Transaction):
    
    index = blockchain.new_transaction(transaction.sender, transaction.recipient, transaction.amount)
    return {"message": f"Transaction will be added to Block {index}"}


@app.get("/chain")
def full_chain():
    
    return {"chain": blockchain.chain, "length": len(blockchain.chain)}



