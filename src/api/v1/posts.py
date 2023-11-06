from typing import Annotated
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB, Credentials
from src.database import Redis
from src.config import log
from src.crud.base import CRUDObject
from src.crud.books import DBBook
from src.crud.users import DBUser
from src.crud.posts import DBPost
from src.model.publications import Post as m_Post
from src.schemas.posts import PostBase, Post
from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/posts", tags=["posts"])

crud_user = DBUser()
crud_book = DBBook()
crud_post = DBPost()


@router.get("/all", summary="Получение всех постов", response_model=Page[Post])
async def get_all(credentials: Credentials, db: DB):
    await checkAuth(db, credentials.credentials)


@router.post("/create", summary="Создание нового поста")
async def add_post_to_db(credentials: Credentials, db: DB, post: PostBase):
    await checkAuth(db, credentials.credentials)

    if not await crud_book.get(db, post.book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная книга не найдена")

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    try:
        post1 = post.dict()
        post_model = m_Post(**(post1))
        post_model.user_id = user_id
        post_model.created_at = datetime.now()
        post_model.updated_at = datetime.now()

        created_post = await crud_post.create(db, post_model, True)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), user)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить пост в БД")

    return created_post


@router.get("/{id}", summary="Получение поста по guid", response_model=Post)
async def get_post_by_id(credentials: Credentials, db: DB, id: UUID):
    await checkAuth(db, credentials.credentials)
