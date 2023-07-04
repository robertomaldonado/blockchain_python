from typing import List

#Initialize an empty line
blockchain = list()
open_transactions = list()
owner = 'Rob'

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
    trasaction = { 'sender': sender,
                   'recipient': recipient, 
                   'amount':amount
                }
    open_transactions.append(trasaction)

def mine_block():
    '''Will be adding a new block'''
    pass

def get_transaction_value() -> float:
    '''Returns user input as a float'''
    tx_recipient = input('Transaction recipient: ')
    tx_amount = float(input('Transaction amount: '))
    return (tx_recipient, tx_amount) 

def get_user_choice() -> float:
    '''Returns user input as a float'''
    return input('User choice: ')

def print_blockchain_elements() -> None:
    '''Outputs the blockchain in blocks'''
    for block in blockchain:
        print(f'B: \n {block}')
    else:
        print('-'*40)

def verify_blockchain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            block_index += 1
            continue
        elif blockchain[block_index][0] == blockchain[block_index-1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid

waiting_for_input = True
while waiting_for_input:

    print(f"Please Choose \n \
          1.Add new transaction \n \
          2.Output blocks \n \
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
        print_blockchain_elements()
    elif user_choice.lower()=='h':
        # Make sure we edit a blockchain that is not empty
        if len(blockchain) >= 1:
            blockchain[0] = [2]
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