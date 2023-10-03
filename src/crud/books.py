from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.books import Book


class DBBook(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Book | None:
        result = await db.execute(select(Book).filter(Book.guid == guid))
        return result.scalars().one_or_none()

    async def get_all(self, db: AsyncSession) -> list[Book]:
        result = await db.execute(select(Book))
        return result.scalars().all()

    async def create(self, db: AsyncSession, Book: Book) -> Book:
        db.add(Book)
        await db.flush()
        await db.commit()
        return Book

    async def update(self, *args):
        pass

    async def delete(self, *args):
        pass
