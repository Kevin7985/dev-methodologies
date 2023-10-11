from fastapi import APIRouter

from src.api.dependency import DB
from src.crud.books import DBAuthor
from src.schemas.books import Author

crud_authors = DBAuthor()

router = APIRouter(prefix="/authors", tags=["authors"], responses={404: {"description": "Not found"}})

@router.get("/authors", summary="Список всех авторов", response_model=list[Author])
async def get_authors(db: DB):
    return await crud_authors.get_all(db)