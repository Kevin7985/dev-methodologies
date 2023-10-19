from fastapi import APIRouter, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB
from src.crud.books import DBAuthor
from src.schemas.books import Author


router = APIRouter(prefix="/authors", tags=["authors"])
DEFAULT_AUTHOR_STRING = Query(default=None, description="Author's name")

crud_authors = DBAuthor()

@router.get("/all", summary="Список всех авторов", response_model=Page[Author])
async def get_all(db: DB):
    return await paginate(db, crud_authors.get_all(db), unique=False)
