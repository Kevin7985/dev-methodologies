from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUDObject
from src.crud.books import DBAuthor, DBGenre
from src.utils.const import AUTHORS_NOT_FOUND, GENRES_NOT_FOUND

crud_objects = CRUDObject()
crud_authors = DBAuthor()
crud_genres = DBGenre()


async def get_authors_or_fail(db: AsyncSession, authors: list[UUID]):
    authors_in_db = await crud_authors.get_many(db, authors)
    if len(authors_in_db) != len(authors):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=AUTHORS_NOT_FOUND)
    return authors_in_db


async def get_genres_or_fail(db: AsyncSession, genres: list[UUID]):
    genres_in_db = await crud_authors.get_many(db, genres)
    if len(genres_in_db) != len(genres):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=GENRES_NOT_FOUND)
    return genres_in_db
