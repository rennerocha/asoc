from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from asoc.finance.db import metadata, start_mappers


start_mappers()

engine = create_engine(
    "sqlite:///",
    connect_args={"check_same_thread": False}
)
get_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


def create_app():
    from asoc.api.routers import router

    app = FastAPI()
    app.include_router(router)

    metadata.create_all(engine)
    return app