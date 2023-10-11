import uuid
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB
from src.crud.books import DBAuthor, DBBook
from src.schemas.books import Author, Book, BookListFilter

router = APIRouter(prefix="/books", tags=["books"], responses={404: {"description": "Not found"}})
DEFAULT_LIST_GENRES = Query(default=None, description="List of genres")
DEFAULT_AUTHOR_STRING = Query(default=None, description="Author's name")

crud_book = DBBook()
crud_authors = DBAuthor()

_CollectionOfOfferFilter = Annotated[BookListFilter, FilterDepends(BookListFilter)]


@router.get("/all", summary="Список всех книг", response_model=Page[Book])
async def get_all(db: DB, book_filter: _CollectionOfOfferFilter, author_name: str | None = DEFAULT_AUTHOR_STRING):
    return await paginate(db, crud_book.get_filtered(book_filter=book_filter, author_name=author_name), unique=False)


@router.get("/{book_id}", summary="Получение книги по guid", response_model=Book)
async def get_book_by_id(db: DB, book_id):
    book_uuid = None
    try:
        book_uuid = uuid.UUID(book_id)
    except:
        return JSONResponse(status_code=400, content={"error": {"code": 400, "message": "Invalid book_id"}})
    
    result = await crud_book.get(db, book_uuid)
    if not result:
        return JSONResponse(status_code=404, content={"error": {"code": 404, "message": "Book not found"}})

    return result


@router.delete("/{book_id}", summary="Удаление книги по guid")
async def delete_book_by_id(db: DB, book_id):
    book_uuid = None
    try:
        book_uuid = uuid.UUID(book_id)
    except:
        return JSONResponse(status_code=400, content={"error": {"code": 400, "message": "Invalid book_id"}})
    
    state = await crud_book.delete(db, book_uuid)
    if not state:
        return JSONResponse(status_code=404, content={"error": {"code": 404, "message": "Book not found"}})

    return {"status": "ok"}


@router.get("/authors", summary="Список всех авторов", response_model=list[Author])
async def get_authors(db: DB):
    return await crud_authors.get_all(db)
