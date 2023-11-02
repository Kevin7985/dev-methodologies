from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUDObject
from src.crud.books import DBAuthor, DBGenre
from src.crud.users import DBUser
from src.model.bookcrossing_points import BookcrossingPoint
from src.utils.const import AUTHORS_NOT_FOUND, GENRES_NOT_FOUND, INVALID_COORDINATES, MAX_LATITUDE, MAX_LONGITUDE

from src.database import Redis

crud_objects = CRUDObject()
crud_authors = DBAuthor()
crud_genres = DBGenre()
crud_user = DBUser()


async def get_authors_or_fail(db: AsyncSession, authors: list[UUID]):
    authors_in_db = await crud_authors.get_many(db, authors)
    if len(authors_in_db) != len(authors):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=AUTHORS_NOT_FOUND)
    return authors_in_db


async def get_genres_or_fail(db: AsyncSession, genres: list[UUID]):
    genres_in_db = await crud_genres.get_many(db, genres)
    if len(genres_in_db) != len(genres):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=GENRES_NOT_FOUND)
    return genres_in_db


async def checkAuth(db: AsyncSession, access_token: str):
    user_id = Redis.get(access_token)
    if not user_id:
        raise HTTPException(403, detail="Not authenticated")

    user_id = UUID(user_id.decode("utf-8"))
    user = await crud_user.get(db, user_id)
    if not user:
        Redis.delete(access_token)
        raise HTTPException(403, detail="Not authenticated")


def validate_coordinates_or_fail(point: BookcrossingPoint) -> None:
    if not (abs(point.latitude) <= MAX_LATITUDE and abs(point.longitude) <= MAX_LONGITUDE):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=INVALID_COORDINATES)
