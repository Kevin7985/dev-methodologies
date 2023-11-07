from uuid import UUID

from sqlalchemy import String, select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.publications import Post


class DBPost(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Post | None:
        return (await db.execute(select(Post).where(Post.guid == guid))).scalars().one_or_none()


    async def create(self, db: AsyncSession, post: Post, with_commit=False) -> Post:
        db.add(post)
        await db.flush()

        if with_commit:
            await db.commit()

        return await self.get(db, post.guid)


    async def delete(self, db: AsyncSession, obj: Book, with_commit=False):
        await db.delete(obj)

        if with_commit:
            await db.commit()
