from dataclasses import dataclass
from typing import Dict

from model import User, ExpenseCalculator


@dataclass
class ExpenseManager:
    """
        driver code which will responsible for saving the transactions
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExpenseManager, cls).__new__(cls)
        return cls._instance

    expense: Dict[str, int] = None
    passbook: Dict[User, Dict[User, int]] = None

    def _update_passbook(self, paid_user, split_users):
        _expense = 0
        if paid_user.user_id in self.passbook:
            _passbook = self.passbook[paid_user.user_id]
            for user, amount in split_users.items():
                if user in _passbook:
                    _passbook[user] += amount
                else:
                    _passbook[user] = amount
                _expense += amount
        else:
            _expense = sum(split_users.values())
            self.passbook[paid_user.user_id] = split_users

        return _expense

    def _update_expense(self, paid_user, expense):
        if paid_user.user_id in self.expense:
            self.expense[paid_user.user_id] += expense
        else:
            self.expense[paid_user.user_id] = expense

    def _update_reverse_passbook(self, paid_user, split_users):
        for user, amount in split_users.items():
            if user in self.passbook:
                if paid_user.user_id in self.passbook[user]:
                    self.passbook[user][paid_user.user_id] -= amount
                else:
                    self.passbook[user][paid_user.user_id] = -amount
            else:
                self.passbook[user] = {paid_user.user_id: -amount}

    def _update_reverse_expense(self,paid_user, split_users):
        for user, amount in split_users.items():
            if paid_user.user_id in self.expense:
                self.expense[paid_user.user_id] -= amount
            else:
                self.expense[paid_user.user_id] = -amount

    def add_expense(self, expense_cal: ExpenseCalculator):

        if not self.expense:
            self.expense = {}
        if not self.passbook:
            self.passbook = {}
        paid_user, split_users = expense_cal.calculate_amount()
        _expense = self._update_passbook(paid_user, split_users)
        self._update_reverse_expense(paid_user, split_users)
        self._update_reverse_passbook(paid_user, split_users)
        self._update_expense(paid_user, _expense)

