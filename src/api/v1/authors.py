from fastapi import APIRouter, HTTPException, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.books import DBAuthor
from src.model.books import Author as m_Author
from src.schemas.books import Author, AuthorBase
from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/authors", tags=["authors"])
DEFAULT_AUTHOR_STRING = Query(default=None, description="Author's name")

crud_authors = DBAuthor()


@router.get("/all", summary="Список всех авторов", response_model=Page[Author])
async def get_all(credentials: Credentials, db: DB, author_name: str | None = None):
    await checkAuth(db, credentials.credentials)
    return await paginate(db, crud_authors.get_all(author_name=author_name), unique=False)


@router.post("/create", summary="Создание нового автора")
async def create_author(credentials: Credentials, db: DB, author: AuthorBase):
    await checkAuth(db, credentials.credentials)

    try:
        author_model = m_Author(**(author.dict()))
        created_author = await crud_authors.create(db, author_model)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), author)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить автора в БД")

    return created_author
