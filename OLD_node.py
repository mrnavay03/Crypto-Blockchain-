from uuid import uuid4
from utility.verification import Verification
from blockchain import Blockchain
from wallet import Wallet

class Node:

    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)


    def get_transaction_value(self):
    # Inputs the new transaction value from the user

        tx_recipient = input('Enter recipient of the transaction: ')
        tx_amount = float(input('Enter transaction amount pls: '))
        return tx_recipient, tx_amount


    def get_user_choice(self):
        """Gets the choice of user; to add new transaction amount,
        print the blockchain or quitting"""

        user_choice = input('Your choice: ')
        return user_choice


    def print_blockchain_elements(self):
        """Prints all elements of the blockchain (all of the blocks are nested lists)"""

        for block in self.blockchain.chain:
            print("Outputting Block ")
            print(block)
        else:
            print('-' * 40)


    def listen_for_input(self):

        waiting_for_input = True

        while waiting_for_input:
            print('Enter choice: ')
            print('1: Add New Transaction Value')
            print('2: Mine a new block')
            print('3: Print the blockchain blocks')
            print('4: Check transaction validity')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save keys')
            print('q: Quit')

            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transactions(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('Transaction successful!')
                else:
                    print('Transaction failed!')
                print(self.blockchain.get_open_transactions())

            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed! Got no wallet?')

            elif user_choice == '3':
                self.print_blockchain_elements()

            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')

            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)

            elif user_choice == '7':
                self.wallet.save_keys()

            elif user_choice == 'q':
                waiting_for_input = False

            else:
                print('Invalid input!! Please enter a valid choice :)')

            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid Blockchain!!')
                break

            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))

        else:
            print('User left')
            print('-' * 40)

        print('Done!!')
        print('-' * 50)

if __name__ == '__main__':   
    node = Node()
    node.listen_for_input()
