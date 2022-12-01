from enums import ExpenseStrategyEnum
from model import PercentExpenseCalculator, ShareExpenseCalculator, ExactExpenseCalculator, User
from database_manager import ExpenseManager
from view import PrintManager

expense_strategy = {
    ExpenseStrategyEnum.EXACT.value: ExactExpenseCalculator,
    ExpenseStrategyEnum.PERCENT.value: PercentExpenseCalculator,
    ExpenseStrategyEnum.SHARE.value: ShareExpenseCalculator
}


def factory(strategy: str):
    if strategy.upper() not in expense_strategy:
        raise ValueError("Invalid expense calculation type")

    return expense_strategy[strategy.upper()]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user1 = User("Abhishek", "Abhishek", 'abhishek.com', 85192254154)
    user2 = User("Rohit", "Rohit", 'abhishek.com', 85192254154)
    user3 = User("Rahul", "Rahul", 'abhishek.com', 85192254154)
    user4 = User("Satyam", "Satyam", 'abhishek.com', 85192254154)
    user5 = User("Umakant", "Umakant", 'abhishek.com', 85192254154)

    strategy = 'Exact'

    strategy_class = factory(strategy)
    strategy_obj = strategy_class(user1, 500, [user5, user2])
    expense_manager = ExpenseManager()
    expense_manager.add_expense(strategy_obj)
    print_manger = PrintManager(expense_manager)
    # print_manger.show_user_expense(user1)

    strategy_class2 = factory('percent')
    strategy_obj2 = strategy_class(user2, 1500, [user1,user3,user5, user2], percents=[10,10, 10,70])
    expense_manager.add_expense(strategy_obj2)
    # print_manger.show_all_transaction()
    print_manger.show_user_expense(user2)
