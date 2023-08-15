from blockchain import Blockchain
from uuid import uuid4
from verification import Verification

class Node:
    def __init__(self) -> None:
        # self.id = str(uuid4())
        self.id = 'Rob'
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self) -> tuple:
        '''Returns user input as a float'''
        tx_recipient = input('Transaction recipient: ')
        tx_amount = float(input('Transaction amount: '))
        return (tx_recipient, tx_amount) 

    def get_user_choice(self) -> str:
        '''Returns user input as a float'''
        return input('User choice: ')

    def print_blockchain_elements(self) -> None:
        '''Outputs the blockchain in blocks'''
        for block in self.blockchain.get_chain():
            print(f'Block: \n {block}')
        else:
            print('-'*40)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            
            print(f"Please Choose \n \
                  1.Add new transaction \n \
                  2.Mine new block \n \
                  3.Output blocks \n \
                  4.Check transactions validity \n \
                  q.Quit"  )
            
            user_choice = self.get_user_choice()
            if user_choice=='1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
            # Add transaction to blockchain
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Successful transaction!!")
                else:
                    print("Transaction failed! :( ")
                print(self.blockchain.get_open_transactions())
            elif user_choice=='2':
                self.blockchain.mine_block()
            elif user_choice=='3':
                self.print_blockchain_elements()
            elif user_choice=='4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('Transactions status OK')
                else:
                    print('There is at least one invalid transaction')
            elif user_choice.lower()=='q':
                # Exit as user has requested
                waiting_for_input = False
            else:
                print("Invalid input. Try again")
            if not Verification.verify_blockchain(self.blockchain.get_chain()):
                self.print_blockchain_elements()
                print("Invalid blockchain!")
                break
            print(f"Balance for {self.id}: {self.blockchain.get_balance():6.2f}")
        else:
            print("User Left!")
        print("Done!")

node = Node()
node.listen_for_input()