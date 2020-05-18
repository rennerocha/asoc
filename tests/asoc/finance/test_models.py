import datetime
import pytest
from asoc.finance.models import Account, Entry, InvalidEntry, InvalidInitialBalance


@pytest.fixture
def account():
    return Account(name="Test Account")


def test_account_with_no_entries_has_balance_zero(account):
    assert account.balance == 0


def test_equal_account_if_same_name():
    account_1 = Account(name="Test Account")
    account_2 = Account(name="Test Account")

    assert account_1 == account_2


def test_newly_account_has_no_entries(account):
    assert account.entries == []


def test_register_entry_increase_account_balance(account):
    entry = Entry("First entry in account", 10)
    account.register(entry)
    assert account.balance == 10


def test_add_new_entry_to_account(account):
    entry = Entry("First entry in account", 10)
    account.register(entry)
    assert entry in account.entries


def test_add_new_entry_with_no_date_defaults_to_today(account):
    entry = Entry("First entry in account", 10)
    account.register(entry)
    assert entry.date == datetime.date.today()


def test_add_new_entry_with_date(account):
    entry = Entry("First entry in account", 10, datetime.date(2020, 7, 28))
    account.register(entry)
    assert entry.date == datetime.date(2020, 7, 28)


def test_add_new_entry_with_negative_amount_to_account(account):
    entry = Entry("First entry in account", 10)
    account.register(entry)

    negative_entry = Entry("Second entry in account", -5)
    account.register(negative_entry)
    assert negative_entry in account.entries


def test_raise_invalid_entry_if_account_balance_may_be_negative(account):
    entry = Entry("First entry in account", -10)
    with pytest.raises(InvalidEntry):
        account.register(entry)


def test_account_may_receive_initial_balance():
    account = Account(name="Test Account", initial_balance=100)
    assert account.balance == 100


def test_account_may_not_receive_negative_initial_balance():
    with pytest.raises(InvalidInitialBalance):
        account = Account(name="Test Account", initial_balance=-100)


def test_able_to_transfer_funds_between_accounts():
    account_1 = Account(name="Test Account 1", initial_balance=100)
    account_2 = Account(name="Test Account 2", initial_balance=100)

    account_1.transfer_funds_to(account_2, 50)

    assert account_1.balance == 50
    assert account_2.balance == 150