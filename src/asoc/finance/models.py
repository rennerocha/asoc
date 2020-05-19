import datetime
from decimal import Decimal
from dataclasses import dataclass, field


class InvalidEntry(Exception):
    ...


class InvalidInitialBalance(Exception):
    ...


class Account:
    def __init__(self, name, initial_balance=0):
        self.name = name
        self.entries = []

        if initial_balance != 0:
            if initial_balance < 0:
                raise InvalidInitialBalance
            self.entries.append(Entry("Initial Balance", initial_balance))

    def __eq__(self, other):
        return self.name == other.name

    def register(self, entry):
        new_balance = self.balance + entry.amount
        if new_balance < 0:
            raise InvalidEntry()
        self.entries.append(entry)

    def transfer_funds_to(self, other, value):
        other.register(Entry("Transfer", value))
        self.register(Entry("Transfer", -1 * value))

    @property
    def balance(self):
        return sum([entry.amount for entry in self.entries])


class Book:
    def __init__(self, name):
        self.name = name


@dataclass(unsafe_hash=True)
class Entry:
    description: str
    amount: Decimal
    date: datetime.date = field(default_factory=datetime.date.today)
