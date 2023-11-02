from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.base import CRUDObject
from src.crud.books import DBAuthor, DBBook, DBBookAuthor, DBBookGenre
from src.model.books import Book as m_Book
from src.model.books import Book_Author, Book_Genre
from src.schemas.books import Author, BookIn, BookListFilter, BookOut, BookUpdate, Book
from src.utils.exceptions import get_authors_or_fail, get_genres_or_fail, checkAuth

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
async def get_all(credentials: Credentials, db: DB, book_filter: _CollectionOfOfferFilter, author_name: str | None = DEFAULT_AUTHOR_STRING):
    await checkAuth(db, credentials.credentials)
    return await paginate(db, crud_book.get_filtered(book_filter=book_filter, author_name=author_name), unique=False)


async def add_genre_book_rows(db: DB, book_guid: UUID, genres: list[UUID]):
    for genre in genres:
        await crud_objects.create(db=db, created_obj=Book_Genre(book_id=book_guid, genre_id=genre))


async def add_authors_book_rows(db: DB, book_guid: UUID, authors: list[UUID]):
    for author in authors:
        await crud_objects.create(db=db, created_obj=Book_Author(book_id=book_guid, author_id=author))


@router.get("/{id}", summary="Получение книги по GUID", response_model=BookOut)
async def get_book_by_id(credentials: Credentials, db: DB, id: UUID):
    await checkAuth(db, credentials.credentials)

    if not (db_book := await crud_book.get(db=db, guid=id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такая книга не найдена")

    try:
        return await crud_book.get(db, id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось получить книгу из БД")


@router.post("/create", summary="Создание новой книги", status_code=status.HTTP_201_CREATED)
async def add_book_to_db(credentials: Credentials, db: DB, book: BookIn):
    await checkAuth(db, credentials.credentials)

    await get_authors_or_fail(db, book.authors)
    await get_genres_or_fail(db, book.genres)
    try:
        book1 = book.dict()
        del book1["authors"]
        del book1["genres"]

        book_model = m_Book(**(book1))
        created_book = await crud_book.create(db=db, book=book_model)
        await add_genre_book_rows(db=db, book_guid=created_book.guid, genres=book.genres)
        await add_authors_book_rows(db=db, book_guid=created_book.guid, authors=book.authors)

        await db.commit()
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), book)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить книгу в БД")
    return await crud_book.get(db, created_book.guid)


@router.put("/update", summary="Обновление книги")
async def update_book(credentials: Credentials, db: DB, book: BookUpdate):
    await checkAuth(db, credentials.credentials)

    if not (db_book := await crud_book.get(db=db, guid=book.guid)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такая книга не найдена")

    await get_authors_or_fail(db, book.authors)
    await get_genres_or_fail(db, book.genres)

    try:
        book_dict = book.dict()
        del book_dict["authors"]
        del book_dict["genres"]

        book_model = Book(**(book_dict))
        updated_book = await crud_book.update(db, book_model)

        await crud_book_genre.delete_by_book(db, book.guid)
        await crud_book_author.delete_by_book(db, book.guid)

        await add_genre_book_rows(db=db, book_guid=book.guid, genres=book.genres)
        await add_authors_book_rows(db=db, book_guid=book.guid, authors=book.authors)

        await db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось обновить книгу в БД")

    return updated_book


@router.delete("/{id}", summary="Удаление книги", status_code=status.HTTP_200_OK)
async def delete_book(credentials: Credentials, db: DB, id: UUID):
    await checkAuth(db, credentials.credentials)

    if not (db_book := await crud_book.get(db=db, guid=id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такая книга не найдена")
    try:
        await crud_book_genre.delete_by_book(db, db_book.guid)
        await crud_book_author.delete_by_book(db, db_book.guid)
        await crud_book.delete(db=db, obj=db_book)

        await db.commit()
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить книгу")
