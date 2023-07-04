from typing import List

#Initialize an empty line
blockchain = list()

def get_last_blockchain_value () -> List[int]:
    '''Return last value of the current blockchain'''
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def add_transaction(transaction_amout: int, last_transaction=[1]) -> None:
    ''' Append new value
        Args: 
            :transaction_amout: Amount to be added
            :last_transaction: Last blockchain transaction (default [1])
    '''
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction,transaction_amout])

def get_transaction_value() -> float:
    '''Returns user input as a float'''
    return float(input('Transaction amount: '))

def get_user_choice() -> float:
    '''Returns user input as a float'''
    return input('User choice: ')

def print_blockchain_elements() -> None:
    '''Outputs the blockchain in blocks'''
    for block in blockchain:
        print(f'B: \n {block}')

def verify_blockchain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index-1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid

while True:

    print(f"Please Choose \n \
          1.Add new transaction \n \
          2.Output blocks \n \
          h.Manipulate blockchain \n \
          q.Quit"  )
    
    user_choice = get_user_choice()
    if user_choice=='1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice=='2':
        print_blockchain_elements()
    elif user_choice.lower()=='h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice.lower()=='q':
        break
    else:
        print("Invalid input. Try again")
    if not verify_blockchain():
        print("Invalid blockchain!")
        break
else:
    print("Done!")