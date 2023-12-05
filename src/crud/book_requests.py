from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.book_requests import BookRequest
from src.schemas.book_requests import BookRequestListFilter


class DBBookRequest(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> BookRequest | None:
        return (await db.execute(select(BookRequest).where(BookRequest.guid == guid))).scalars().one_or_none()


    async def create(self, db: AsyncSession, req: BookRequest, with_commit=False) -> BookRequest:
        db.add(req)
        await db.flush()

        if with_commit:
            await db.commit()

        return await self.get(db, req.guid)


    async def get_filtered(self, req_filter: BookRequestListFilter):
        query = req_filter.filter(select(BookRequest))

        return query
