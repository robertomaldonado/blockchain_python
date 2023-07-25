from functools import reduce
import hashlib as hl
import json
from typing import List

MINING_REWARD = 10

genesis_block = {'previous_hash': '', 'index': 0, 'transactions': []}
blockchain = [genesis_block]
open_transactions = list()
owner = 'Rob'
participants = set()

def hash_block(block) -> str:
    '''Retun a string representation of the transaction
    Args:
        :block: The current block to represent
    '''
    return hl.sha256(json.dumps(block).encode()).hexdigest()
 
def get_balance(participant) -> int:
    '''Returns the balance for a given participant'''
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender  = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    
    return amount_received - amount_sent

def get_last_blockchain_value () -> List[int]:
    '''Return last value of the current blockchain'''
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def verify_transaction(transaction)-> bool:
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

def add_transaction(recipient, sender=owner, amount=1.0) -> None:
    ''' Append new value
        Args: 
            :sender: Sender of transaction
            :recepient: Recipient of transaction
            :amout: Amount sent in transaction
    '''
    transaction = { 'sender': sender,
                   'recipient': recipient, 
                   'amount':amount
                }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block() -> bool:
    '''Will be adding a new block'''
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print(hashed_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': copied_transactions
            }
    blockchain.append(block)
    return True

def get_transaction_value() -> tuple:
    '''Returns user input as a float'''
    tx_recipient = input('Transaction recipient: ')
    tx_amount = float(input('Transaction amount: '))
    return (tx_recipient, tx_amount) 

def get_user_choice() -> str:
    '''Returns user input as a float'''
    return input('User choice: ')

def print_blockchain_elements() -> None:
    '''Outputs the blockchain in blocks'''
    for block in blockchain:
        print(f'B: \n {block}')
    else:
        print('-'*40)

def verify_blockchain() -> bool:
    '''Verfy chain'''
    for (index, block) in enumerate(blockchain):
        if index == 0: continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True

def verify_transactions() -> bool:
    return all([verify_transaction(tx) for tx in open_transactions])

waiting_for_input = True
while waiting_for_input:

    print(f"Please Choose \n \
          1.Add new transaction \n \
          2.Mine new block \n \
          3.Output blocks \n \
          4.List participants \n \
          5.Check transactions validity \n \
          h.Manipulate blockchain \n \
          q.Quit"  )
    
    user_choice = get_user_choice()
    if user_choice=='1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
    # Add transaction to blockchain
        if add_transaction(recipient, amount=amount):
            print("Successful transaction!!")
        else:
            print("Transaction failed! :( ")
        print(open_transactions)
    elif user_choice=='2':
        if mine_block():
            open_transactions = []
    elif user_choice=='3':
        print_blockchain_elements()
    elif user_choice=='4':
        print(participants)
    elif user_choice=='5':
        if verify_transactions():
            print('Transactions status OK')
        else:
            print('There is at least one invalid transaction')
    elif user_choice.lower()=='h':
        # Make sure we edit a blockchain that is not empty
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender':'Bob', 'recipient':'Rob', 'amount':1000.0}]
            }
    elif user_choice.lower()=='q':
        # Exit as user has requested
        waiting_for_input = False
    else:
        print("Invalid input. Try again")
    if not verify_blockchain():
        print_blockchain_elements()
        print("Invalid blockchain!")
        break
    print(f"Balance for {owner}: {get_balance(owner):6.2f}")
else:
    print("User Left!")

print("Done!")