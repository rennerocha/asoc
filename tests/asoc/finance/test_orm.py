import datetime
import uuid
from decimal import Decimal

from asoc.finance.models import Account, Book, Entry


def test_can_add_book_with_mapping(session):
    book_code = uuid.uuid4().hex
    book = Book(code=book_code, name="New Book")
    session.add(book)
    session.commit()

    rows = list(session.execute('SELECT code, name FROM "books"'))
    assert rows == [(book_code, "New Book",)]


def test_can_add_account_with_mapping(session):
    account = Account(name="Test Account")
    session.add(account)
    session.commit()

    rows = list(session.execute('SELECT name FROM "accounts"'))
    assert rows == [("Test Account",)]


def test_can_add_account_with_initial_balance(session):
    account = Account(name="Test Account", initial_balance=42.01)
    session.add(account)
    session.commit()

    balance = session.execute(
        'SELECT initial_balance FROM "accounts" WHERE name = "Test Account"'
    ).fetchone()
    assert balance == (42.01,)


def test_can_retrieve_account_with_mapping(session):
    session.execute(
        """INSERT INTO accounts (name) VALUES
        ("First Account"),
        ("Second Account");"""
    )
    expected = [
        Account(name="First Account"),
        Account(name="Second Account"),
    ]
    assert session.query(Account).all() == expected


def test_entry_is_stored_with_its_account(session):
    account = Account("Test Account")
    entry = Entry("First Entry", Decimal("10"), datetime.date(2020, 4, 27))
    account.register(entry)
    session.add(account)
    session.commit()

    selected_entry = session.query(Entry).one()
    assert selected_entry.account == account


def test_entries_mapper_can_load_lines(session):
    session.execute(
        """INSERT INTO entries (description, amount, date) VALUES
        ("First Entry", 10, "2020-04-27"),
        ("Second Entry", 10.42, "2020-04-27"),
        ("Third Entry", 20.02, "2020-04-27");"""
    )
    expected = [
        Entry("First Entry", Decimal("10"), datetime.date(2020, 4, 27)),
        Entry("Second Entry", Decimal("10.42"), datetime.date(2020, 4, 27)),
        Entry("Third Entry", Decimal("20.02"), datetime.date(2020, 4, 27)),
    ]
    assert session.query(Entry).all() == expected


def test_entry_mapper_can_save_lines(session):
    new_entry = Entry("Test Entry", 10)
    session.add(new_entry)
    session.commit()

    rows = list(session.execute('SELECT description, amount FROM "entries"'))
    assert rows == [("Test Entry", 10)]


def test_can_add_book_with_with_mapping(session):
    book = Book(code=uuid.uuid4().hex, name="New Book")
    account = Account(name="Test Account")
    book.register(account)

    session.add(book)
    session.commit()

    account = session.query(Account).one()
    assert account.book == book
