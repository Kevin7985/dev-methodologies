from typing import Annotated
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB, Credentials
from src.database import Redis
from src.config import log
from src.crud.books import DBBook
from src.crud.users import DBUser
from src.crud.posts import DBPost
from src.crud.posts import DBComment
from src.model.publications import PostComment as m_Comment
from src.schemas.posts import PostCommentBase, PostCommentIn, PostComment
from src.utils.exceptions import checkAuth

router = APIRouter(prefix = "/posts", tags=["post comments"])

crud_user = DBUser()
crud_book = DBBook()
crud_post = DBPost()
crud_comment = DBComment()


@router.get("/{post_id}/comments", summary="Получение комментариев к посту", response_model=Page[PostComment])
async def get_comments(credentials: Credentials, db: DB, post_id: UUID):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    if not await crud_post.get(db, post_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пост с данным guid не найден")

    return await paginate(db, await crud_comment.get_by_post_id(db, post_id), unique=False)


@router.post("/{post_id}/comments/add", summary="Добавление нового комментария", response_model=PostComment)
async def add_comment(credentials: Credentials, db: DB, post_id: UUID, comment: PostCommentIn):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    if not await crud_post.get(db, post_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пост с данным guid не найден")

    try:
        comment1 = comment.dict()
        comment_model = m_Comment(**(comment1))
        comment_model.user_id = user_id
        comment_model.post_id = post_id
        comment_model.created_at = datetime.now()

        created_comment = await crud_comment.add(db, comment_model, True)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), comment)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить коммент в БД")

    return created_comment


@router.get("/comments/{id}", summary="Получение комментария по guid", response_model=PostComment)
async def get_comment_by_id(credentials: Credentials, db: DB, id: UUID):
    await checkAuth(db, credentials.credentials)

    if not (db_comment := await crud_comment.get(db, id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный комментарий не найден")

    return db_comment


@router.delete("/comments/{id}", summary="Удаление комментария по guid")
async def delete_comment(credentials: Credentials, db: DB, id: UUID):
    await checkAuth(db, credentials.credentials)

    if not (db_comment := await crud_comment.get(db, id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный комментарий не найден")

    try:
        await crud_comment.delete(db, id, True)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить комментарий")
