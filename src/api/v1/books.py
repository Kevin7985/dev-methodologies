from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB
from src.crud.books import DBBook
from src.schemas.books import Book, BookListFilter
from src.utils.const import GenreEnum

router = APIRouter(prefix="/books", tags=["books"], responses={404: {"description": "Not found"}})
DEFAULT_LIST_GENRES = Query(default=None, description="List of genres")
DEFAULT_LIST_AUTHORS = Query(default=None, description="List of authors' GUIDs")

crud_book = DBBook()

_CollectionOfOfferFilter = Annotated[BookListFilter, FilterDepends(BookListFilter)]


@router.get("/all", summary="Список всех книг", response_model=Page[Book])
async def get_all(
    db: DB,
    book_filter: _CollectionOfOfferFilter,
    genre: list[GenreEnum] | None = DEFAULT_LIST_GENRES,
    authors: list[UUID] | None = DEFAULT_LIST_AUTHORS,
):
    return await paginate(
        db, crud_book.get_filtered(book_filter=book_filter, genre=genre, authors=authors), unique=False
    )
