from uuid import UUID
from fastapi import APIRouter

from src.api.dependency import DB
from src.crud.books import DBBook
from src.schemas.books import Book, BookListFilter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from typing import Annotated
from fastapi_pagination.ext.sqlalchemy import paginate

from src.utils.const import GenreEnum

router = APIRouter(prefix="/books", tags=["books"], responses={404: {"description": "Not found"}})
crud_book = DBBook()

_CollectionOfOfferFilter = Annotated[BookListFilter, FilterDepends(BookListFilter)]

@router.get("/all", summary="Список всех книг", response_model=Page[Book])
async def get_all(db: DB, book_filter: _CollectionOfOfferFilter, genre: list[GenreEnum] | None, authors: list[UUID] | None):
    return await paginate(db, crud_book.get_filtered(book_filter=book_filter, genre=genre, authors=authors))
