from fastapi import APIRouter

from src.api.dependency import DB
from src.crud.books import DBBook
from src.schemas.books import Book

router = APIRouter(prefix="/books", tags=["books"], responses={404: {"description": "Not found"}})
crud_book = DBBook()


@router.get("/all", summary="Список всех книг", response_model=list[Book])
async def get_all(db: DB):
    return await crud_book.get_all(db)
