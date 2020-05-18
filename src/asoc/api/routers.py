from fastapi import APIRouter
from sqlalchemy.orm import Session

from asoc.api import get_session
from asoc.finance.db import Book

router = APIRouter()


@router.get("/")
async def read_main():
    return {"msg": "Hello World"}


@router.get("/books")
async def books():
    session = get_session()
    return session.query(Book).all()
