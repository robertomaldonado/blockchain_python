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

class Blockchain:
    def __init__(self) -> None:
        #Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Init empty blockchain list
        self.chain = [genesis_block]
        # Unhandled transactions
        self.open_transactions = list()
        self.load_data()

    def load_data(self):
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
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.open_transactions = updated_transactions
        except (IOError, IndexError):
            print("Esception handled")
        finally:
            print("Clean up!")

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                saveable_chain = [block.__dict__ for block in 
                                [Block(block_el.index, block_el.previous_hash, 
                                        [tx.__dict__ for tx in block_el.transactions],block_el.proof, block_el.timestamp) 
                                for block_el in self.chain ]]
                f.write(json.dumps(saveable_chain))
                f.write("\n")
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
                # save_data = { 'chain': blockchain, 'ot': open_transactions}
                # f.write(pickle.dumps(save_data))
        except IOError:
            print("Saving failed!")

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        verifier = Verification()
        while not verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof
 
    def get_balance(self, participant) -> int:
        '''Returns the balance for a given participant'''
        tx_sender = [[tx.amount for tx in block.transactions 
                    if tx.sender == participant] for block in self.chain]
        open_tx_sender  = [tx.amount
                        for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                            if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions 
                        if tx.recipient == participant] for block in self.chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                                if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        
        return amount_received - amount_sent

    def get_last_blockchain_value (self) -> List[int]:
        '''Return last value of the current blockchain'''
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0) -> None:
        ''' Append new value
            Args: 
                :sender: Sender of transaction
                :recepient: Recipient of transaction
                :amout: Amount sent in transaction
        '''
        transaction = Transaction(sender, recipient, amount)
        verifier = Verification()
        if verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self, node) -> bool:
        '''Will be adding a new block'''
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', node, MINING_REWARD)
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain), hashed_block, copied_transactions, proof)
        self.chain.append(block)
        return True
