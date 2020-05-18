from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper

metadata = MetaData()

books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255))
)

class Book:
    def __init__(self, name):
        self.name = name


def start_mappers():
    mapper(Book, books)