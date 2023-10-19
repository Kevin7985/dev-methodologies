from fastapi import APIRouter, Query, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB
from src.crud.books import DBAuthor
from src.schemas.books import Author, AuthorBase
from src.model.books import Author as m_author


router = APIRouter(prefix="/authors", tags=["authors"])
DEFAULT_AUTHOR_STRING = Query(default=None, description="Author's name")

crud_authors = DBAuthor()


@router.get("/all", summary="Список всех авторов", response_model=Page[Author])
async def get_all(db: DB):
    return await paginate(db, crud_authors.get_all(db), unique=False)


@router.post("/create", summary="Создание нового автора")
async def create_author(db: DB, author: AuthorBase):
    try:
        author_model = m_author(**(author.dict()))
        created_author = await crud_authors.create(db, author_model)
        print(created_author)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить автора в БД")

    return created_author
