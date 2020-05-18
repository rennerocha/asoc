from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy import (
    Table, Column, Numeric, Integer, String, Date, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from asoc.finance.models import Account, Book, Entry


metadata = MetaData()

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255))
)


accounts = Table(
    "accounts", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255))
)


entries = Table(
    "entries", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("account_id", Integer, ForeignKey("accounts.id")),
    Column("description", String(255)),
    Column("amount", Numeric(10, 2)),
    Column("date", Date),
)


def start_mappers():
    mapper(Book, books)
    mapper(Entry, entries)
    mapper(Account, accounts, properties={
        "entries": relationship(Entry, backref="account")
    })
