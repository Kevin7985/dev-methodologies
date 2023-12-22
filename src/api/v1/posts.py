from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.books import DBBook
from src.crud.posts import DBPost
from src.crud.users import DBUser
from src.database import Redis
from src.model.publications import Post as m_Post
from src.schemas.posts import PostAllInfo, PostBase, PostListFilter
from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/posts", tags=["posts"])

crud_user = DBUser()
crud_book = DBBook()
crud_post = DBPost()

_CollectionOfOfferFilter = Annotated[PostListFilter, FilterDepends(PostListFilter)]


@router.get("/all", summary="Получение всех постов", response_model=Page[PostAllInfo])
async def get_all(credentials: Credentials, db: DB, postFilter: _CollectionOfOfferFilter):
    # await checkAuth(db, credentials.credentials)

    return await paginate(db, await crud_post.get_filtered(postFilter), unique=False)


@router.post("/create", summary="Создание нового поста", response_model=PostAllInfo)
async def add_post_to_db(credentials: Credentials, db: DB, post: PostBase):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    if (post.book_id) and (not await crud_book.get(db, post.book_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга с данным guid не найдена")

    try:
        post1 = post.dict()
        post_model = m_Post(**(post1))
        post_model.user_id = user_id
        post_model.created_at = datetime.now()
        post_model.updated_at = datetime.now()

        created_post = await crud_post.create(db, post_model, True)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), post)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить пост в БД")

    return created_post


@router.get("/{id}", summary="Получение поста по guid", response_model=PostAllInfo)
async def get_post_by_id(credentials: Credentials, db: DB, id: UUID):
    # await checkAuth(db, credentials.credentials)

    if not (db_post := await crud_post.get(db, id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный пост не найден")

    return db_post


@router.put("/update", summary="Обновление поста")
async def update_post(credentials: Credentials, db: DB, post: PostBase):
    await checkAuth(db, credentials.credentials)

    if not (await crud_post.get(db, post.guid)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный пост не найден")

    if (post.book_id) and (not await crud_book.get(db, post.book_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга с данным guid не найдена")

    try:
        post1 = post.dict()
        post_model = m_Post(**(post1))
        post_model.updated_at = datetime.now()
        updated_post = await crud_post.update(db, post_model, True)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), post)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось обновить пост в БД")

    return updated_post


@router.delete("/{id}", summary="Удаление поста по guid")
async def delete_post(credentials: Credentials, db: DB, id: UUID):
    # await checkAuth(db, credentials.credentials)

    if not (db_post := await crud_post.get(db, id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный пост не найден")

    try:
        await crud_post.delete(db, db_post, True)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить пост")
