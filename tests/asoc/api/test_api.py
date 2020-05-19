import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, clear_mappers

from asoc.api import create_app, get_session
from asoc.finance.db import Book, start_mappers, metadata



@pytest.fixture
def app(in_memory_db):
    app = create_app(testing=True)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def book(session):
    new_book = Book(name="LHC 2020")
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    yield new_book


def test_api_version(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_database_access(client, book, session):
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_database_access_again(client, book, session):
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1
