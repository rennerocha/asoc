import pytest
from dynaconf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from asoc.finance.db import metadata, start_mappers


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture
def in_memory_db():
    engine = create_engine(
        settings.DATABASE_URI, connect_args={"check_same_thread": False}
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
