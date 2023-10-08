from typing import Annotated

from fastapi import APIRouter, Query
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB
from src.crud.books import DBAuthor, DBBook
from src.schemas.books import Author, Book, BookListFilter
from src.utils.const import GenreEnum

router = APIRouter(prefix="/books", tags=["books"], responses={404: {"description": "Not found"}})
DEFAULT_LIST_GENRES = Query(default=None, description="List of genres")
DEFAULT_AUTHOR_STRING = Query(default=None, description="Author's name")

crud_book = DBBook()
crud_authors = DBAuthor()

_CollectionOfOfferFilter = Annotated[BookListFilter, FilterDepends(BookListFilter)]


@router.get("/all", summary="Список всех книг", response_model=Page[Book])
async def get_all(
    db: DB,
    book_filter: _CollectionOfOfferFilter,
    genre: list[GenreEnum] | None = DEFAULT_LIST_GENRES,
    author_name: str | None = DEFAULT_AUTHOR_STRING,
):
    return await paginate(
        db, crud_book.get_filtered(book_filter=book_filter, genre=genre, author_name=author_name), unique=False
    )


@router.get("/authors", summary="Список всех авторов", response_model=list[Author])
async def get_authors(db: DB):
    return await crud_authors.get_all(db)
