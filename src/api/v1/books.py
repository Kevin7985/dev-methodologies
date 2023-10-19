from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB
from src.config import log
from src.crud.base import CRUDObject
from src.crud.books import DBAuthor, DBBook, DBBookAuthor, DBBookGenre
from src.model.books import Book as m_Book
from src.model.books import Book_Author, Book_Genre
from src.schemas.books import Author, BookIn, BookListFilter, BookOut
from src.utils.exceptions import get_authors_or_fail, get_genres_or_fail

router = APIRouter(prefix="/books", tags=["books"], responses={404: {"description": "Not found"}})
DEFAULT_LIST_GENRES = Query(default=None, description="List of genres")
DEFAULT_AUTHOR_STRING = Query(default=None, description="Author's name")

crud_book = DBBook()
crud_authors = DBAuthor()
crud_objects = CRUDObject()
crud_book_genre = DBBookGenre()
crud_book_author = DBBookAuthor()

_CollectionOfOfferFilter = Annotated[BookListFilter, FilterDepends(BookListFilter)]


@router.get("/all", summary="Список всех книг", response_model=Page[BookOut])
async def get_all(db: DB, book_filter: _CollectionOfOfferFilter, author_name: str | None = DEFAULT_AUTHOR_STRING):
    return await paginate(db, crud_book.get_filtered(book_filter=book_filter, author_name=author_name), unique=False)


async def add_genre_book_rows(db: DB, book_guid: UUID, genres: list[UUID]):
    for genre in genres:
        await crud_objects.create(db=db, created_obj=Book_Genre(book_id=book_guid, genre_id=genre))


async def add_authors_book_rows(db: DB, book_guid: UUID, authors: list[UUID]):
    for author in authors:
        await crud_objects.create(db=db, created_obj=Book_Author(book_id=book_guid, author_id=author))


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def add_book_to_db(db: DB, book: BookIn):
    await get_authors_or_fail(db, book.authors)
    await get_genres_or_fail(db, book.genres)
    try:
        book_model = m_Book(**(book.book_fields.dict()))
        created_book = await crud_book.create(db=db, book=book_model)
        await add_genre_book_rows(db=db, book_guid=created_book.guid, genres=book.genres)
        await add_authors_book_rows(db=db, book_guid=created_book.guid, authors=book.authors)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), book)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить книгу в БД")
    return created_book


@router.post("/delete", summary="Удалить книгу", status_code=status.HTTP_200_OK)
async def delete_book(db: DB, guid: UUID):
    if not (db_book := await crud_book.get(db=db, guid=guid)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такая книга не найдена")
    try:
        await crud_book_genre.delete_by_book(db, db_book.guid)
        await crud_book_author.delete_by_book(db, db_book.guid)
        await crud_book.delete(db=db, obj=db_book)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить книгу")
