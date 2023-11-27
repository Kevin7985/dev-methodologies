from typing import Annotated
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_filter import FilterDepends
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

@router.post("/{post_id}/comments/add", summary="Добавление нового комментария")
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
        print(created_comment.__dict__)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), comment)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить коммент в БД")

    return created_comment
