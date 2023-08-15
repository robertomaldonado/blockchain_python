class Node:
    def __init__(self) -> None:
        self.blockchain = []

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
        for block in self.blockchain:
            print(f'B: \n {block}')
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
                if add_transaction(recipient, amount=amount):
                    print("Successful transaction!!")
                else:
                    print("Transaction failed! :( ")
                print(open_transactions)
            elif user_choice=='2':
                if mine_block():
                    open_transactions = []
                    save_data()
            elif user_choice=='3':
                self.print_blockchain_elements()
            elif user_choice=='4':
                verifier = Verification()
                if verifier.verify_transactions(open_transactions, get_balance):
                    print('Transactions status OK')
                else:
                    print('There is at least one invalid transaction')
            elif user_choice.lower()=='q':
                # Exit as user has requested
                waiting_for_input = False
            else:
                print("Invalid input. Try again")
            verifier = Verification()
            if not verifier.verify_blockchain(blockchain):
                self.print_blockchain_elements()
                print("Invalid blockchain!")
                break
            print(f"Balance for {owner}: {get_balance(owner):6.2f}")
        else:
            print("User Left!")
        print("Done!")
                