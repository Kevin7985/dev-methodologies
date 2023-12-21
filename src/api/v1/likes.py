from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.posts import DBLike, DBPost
from src.crud.users import DBUser
from src.database import Redis
from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/posts", tags=["post likes"])

crud_user = DBUser()
crud_post = DBPost()
crud_post_like = DBLike()


@router.post("/{post_id}/like", summary="Добавление лайка посту")
async def add_like(credentials: Credentials, db: DB, post_id: UUID):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    if not (await crud_post.get(db, post_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный пост не найден")

    try:
        likes = await crud_post_like.get(db, post_id)
        if user_id in likes:
            return

        await crud_post_like.add(db, user_id, post_id, True)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить лайк в БД")


@router.get("/{post_id}/likes", summary="Получение лайков к посту")
async def get_likes(credentials: Credentials, db: DB, post_id: UUID) -> list[UUID]:
    await checkAuth(db, credentials.credentials)

    if not (await crud_post.get(db, post_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный пост не найден")

    try:
        return await crud_post_like.get(db, post_id)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось получить лайки в БД")


@router.delete("/{post_id}/like", summary="Удаление лайка у поста")
async def delete_like(credentials: Credentials, db: DB, post_id: UUID):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    if not (await crud_post.get(db, post_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный пост не найден")

    try:
        likes = await crud_post_like.get(db, post_id)
        if user_id not in likes:
            return

        await crud_post_like.delete(db, user_id, post_id, True)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить лайк из БД")
