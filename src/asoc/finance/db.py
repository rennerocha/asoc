from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
)
from sqlalchemy.orm import mapper, relationship

from asoc.finance.models import Account, Book, Entry

metadata = MetaData()

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("code", String(255)),
    Column("name", String(255)),
)


accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("name", String(255)),
    Column("initial_balance", Numeric(10, 2)),
)


entries = Table(
    "entries",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("account_id", Integer, ForeignKey("accounts.id")),
    Column("description", String(255)),
    Column("amount", Numeric(10, 2)),
    Column("date", Date),
)


def start_mappers():
    mapper(
        Book,
        books,
        properties={
            "accounts": relationship(Account, backref="book", collection_class=set)
        },
    )
    mapper(Entry, entries)
    mapper(
        Account,
        accounts,
        properties={"entries": relationship(Entry, backref="account")},
    )
