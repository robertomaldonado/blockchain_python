from typing import List

#Initialize an empty line
genesis_block = {'previous_hash': '', 'index': 0, 'transactions': []}
blockchain = [genesis_block]
open_transactions = list()
owner = 'Rob'

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

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
    transaction = { 'sender': sender,
                   'recipient': recipient, 
                   'amount':amount
                }
    open_transactions.append(transaction)

def mine_block() -> None:
    '''Will be adding a new block'''
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': open_transactions
            }
    blockchain.append(block)

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

waiting_for_input = True
while waiting_for_input:

    print(f"Please Choose \n \
          1.Add new transaction \n \
          2.Mine new block \n \
          3.Output blocks \n \
          h.Manipulate blockchain \n \
          q.Quit"  )
    
    user_choice = get_user_choice()
    if user_choice=='1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
    # Add transaction to blockchain
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice=='2':
        mine_block()
    elif user_choice=='3':
        print_blockchain_elements()
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
else:
    print("User Left!")

print("Done!")