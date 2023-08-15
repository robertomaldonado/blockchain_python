from functools import reduce
import hashlib as hl
from typing import List
import json
# import pickle
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10
# Init empty blockchain list
blockchain = []
# Unhandled transactions
open_transactions = list()
owner = 'Rob'
participants = {owner}

def load_data():
    global blockchain
    global open_transactions
    try:
        with open("blockchain.txt", mode="r") as f:
            # file_content = pickle.loads(f.read())
            # global blockchain
            # global open_transactions
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']
            file_content = f.readlines()
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        #Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Init empty blockchain list
        blockchain = [genesis_block]
        # Unhandled transactions
        open_transactions = list()
    finally:
        print("Clean up!")

load_data()

def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            saveable_chain = [block.__dict__ for block in 
                              [Block(block_el.index, block_el.previous_hash, 
                                     [tx.__dict__ for tx in block_el.transactions],block_el.proof, block_el.timestamp) 
                               for block_el in blockchain ]]
            f.write(json.dumps(saveable_chain))
            f.write("\n")
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
            # save_data = { 'chain': blockchain, 'ot': open_transactions}
            # f.write(pickle.dumps(save_data))
    except IOError:
        print("Saving failed!")

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof
 
def get_balance(participant) -> int:
    '''Returns the balance for a given participant'''
    tx_sender = [[tx.amount for tx in block.transactions 
                  if tx.sender == participant] for block in blockchain]
    open_tx_sender  = [tx.amount
                       for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                         if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx.amount for tx in block.transactions 
                     if tx.recipient == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                             if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    
    return amount_received - amount_sent

def get_last_blockchain_value () -> List[int]:
    '''Return last value of the current blockchain'''
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def add_transaction(recipient, sender=owner, amount=1.0) -> None:
    ''' Append new value
        Args: 
            :sender: Sender of transaction
            :recepient: Recipient of transaction
            :amout: Amount sent in transaction
    '''
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        # participants.add(sender)
        # participants.add(recipient)
        save_data()
        return True
    return False

def mine_block() -> bool:
    '''Will be adding a new block'''
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True
