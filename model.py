from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from errors import InvalidShareParams, InvalidPercentParams


@dataclass
class User:
    """
    User implementations of the  User Schema which will store the data of the user
    """
    user_id: str
    name: str
    email: str
    contact: int

    def __str__(self):
        return self.name


class ExpenseCalculator(ABC):
    """abstract class for the Expense calculation strategy"""

    @abstractmethod
    def __init__(self, paid_user: User, amount: int, owe_user: List[User], **kwargs):
        pass

    @abstractmethod
    def calculate_amount(self) -> Tuple[User,Dict]:

        """
            abstract function which will responsible for further implementation of the Expense strategy
            amount calculation
            :return: Tuple of user and its transactions
        """


class ExactExpenseCalculator(ExpenseCalculator):

    def __init__(self, paid_user: User, amount: int, owe_user: List[User], **kwargs):
        self.paid_user = paid_user
        self.amount = amount
        self.owe_user = owe_user

    def calculate_amount(self) -> Tuple[User, Dict]:
        """ implementation of the expense calculation which is equally divide into all users """
        number_of_user = len(self.owe_user)
        each_share = self.amount / number_of_user
        balance_sheet = dict()
        for user in self.owe_user:
            if user != self.paid_user:
                balance_sheet[user.user_id] = each_share
        return self.paid_user, balance_sheet


class ShareExpenseCalculator(ExpenseCalculator):

    def __init__(self, paid_user: User, amount: int, owe_user: List[User], **kwargs):
        self.paid_user = paid_user
        self.amount = amount
        self.owe_user = owe_user
        self.shares = kwargs.get('shares', None)

    def validate_share(self) -> None:
        if sum(self.shares) != self.amount:
            raise InvalidShareParams("total amount of share passed is not matching with the total amount")
        if len(self.shares) != len(self.owe_user):
            raise InvalidShareParams("length of the share is not matching with the user array")

    def calculate_amount(self) -> Tuple[User, Dict]:
        """
            implementation of the expense calculation which is equally divide on the basis of share amount.
        :param paid_user: user who paid
        :param amount: amount the user paid
        :param owe_user: list of the user among which the amount divide
        :param kwargs: keyword arguments
        :return:
        """
        if self.shares is None:
            raise InvalidShareParams("please pass the valid share params")
        self.validate_share()
        balance_sheet = dict()
        for user, share in self.owe_user, self.shares:
            if user != self.paid_user:
                balance_sheet[user.id] = share
        return self.paid_user, balance_sheet


class PercentExpenseCalculator(ExpenseCalculator):

    def __init__(self, paid_user: User, amount: int, owe_user: List[User], **kwargs):
        self.paid_user = paid_user
        self.amount = amount
        self.owe_user = owe_user
        self.percents = kwargs.get('percents', None)

    def validate_share(self) -> None:
        if sum(self.percents) != 100:
            raise InvalidPercentParams("total amount of share passed is not matching with the total amount")
        if len(self.percents) != len(self.owe_user):
            raise InvalidPercentParams("length of the share is not matching with the user array")

    def calculate_amount(self) -> Tuple[User, Dict]:
        """
            implementation of the expense calculation which is equally divide on the basis of percent.
        """
        if self.percents is None:
            raise InvalidPercentParams("please pass the valid percent params")
        self.validate_share()
        balance_sheet = dict()
        for user, percent in self.owe_user, self.percents:
            if user != self.paid_user:
                balance_sheet[user.id] = (percent * self.amount) / 100
        return self.paid_user, balance_sheet
