import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from asoc.finance.db import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine(
        "sqlite:///test.db", connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
    yield engine
    metadata.drop_all(engine)


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    db = sessionmaker(bind=in_memory_db)()
    yield db
    clear_mappers()
    db.close()
