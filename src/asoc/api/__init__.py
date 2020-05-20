from dynaconf import settings
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from asoc.finance.db import metadata, start_mappers


def get_db_engine():
    return create_engine(
        settings.DATABASE_URI, connect_args={"check_same_thread": False},
    )


def get_session():
    engine = get_db_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


def get_db():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


def create_app(testing=False):
    from asoc.api.routers import router

    if not testing:
        start_mappers()

    engine = get_db_engine()
    metadata.create_all(engine)

    app = FastAPI()
    app.include_router(router)

    return app
