from model import User
from database_manager import ExpenseManager


class PrintManager:
    """
    class responsible for printing the pass book
    """

    def __init__(self, database: ExpenseManager):
        self.database = database

    def show_user_expense(self, user: User):

        if user.user_id not in self.database.expense or \
                user.user_id not in self.database.passbook:
            print('No expense is present for that user')
            return
        print(f'{user.name} having expense of {self.database.expense.get(user.user_id)}')
        print('list of transactions')
        for key, val in self.database.passbook[user.user_id].items():
            print(f'{user.name} owe {val} from {key}')

    def show_all_transaction(self):
        if not self.database.expense or not self.database.passbook:
            print("No transaction found")
            return
        print("list of all transaction")
        for paid_user, passbook in self.database.passbook.items():
            for owe_user, amount in passbook.items():
                print(f'{paid_user} owe {amount} from {owe_user}')
