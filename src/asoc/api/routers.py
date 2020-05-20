from fastapi import APIRouter

from asoc import __version__
from asoc.api import get_session
from asoc.finance.db import Book

router = APIRouter()


@router.get("/")
async def read_main():
    return {"version": __version__}


@router.get("/books")
async def books():
    session = get_session()
    return session.query(Book).all()
