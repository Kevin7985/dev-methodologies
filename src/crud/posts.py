from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.publications import Post, PostLike
from src.schemas.posts import PostListFilter


class DBPost(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Post | None:
        return (await db.execute(select(Post).where(Post.guid == guid))).scalars().one_or_none()

    async def create(self, db: AsyncSession, post: Post, with_commit=False) -> Post:
        db.add(post)
        await db.flush()

        if with_commit:
            await db.commit()

        return await self.get(db, post.guid)

    async def update(self, db: AsyncSession, obj: Post, with_commit=False) -> Post:
        update_query = (
            sql_update(Post.__table__)
            .where(Post.guid == obj.guid)
            .values(
                {
                    "book_id": obj.book_id,
                    "title": obj.title,
                    "type": obj.type,
                    "book_rating": obj.book_rating,
                    "updated_at": obj.updated_at,
                }
            )
        )

        await db.execute(update_query)
        await db.flush()

        if with_commit:
            await db.commit()

        return await self.get(db, obj.guid)

    async def delete(self, db: AsyncSession, obj: Post, with_commit=False):
        await db.delete(obj)

        if with_commit:
            await db.commit()

    async def get_filtered(self, post_filter: PostListFilter):
        query = post_filter.filter(select(Post))

        return query


class DBLike(CRUD):
    async def get(self, db: AsyncSession, post_id: UUID):
        data = (await db.execute(select(PostLike).where(PostLike.post_id == post_id))).scalars().all()
        return [like.user_id for like in data]

    async def getByIds(self, db: AsyncSession, user_id: UUID, post_id: UUID):
        return (
            (await db.execute(select(PostLike).where(PostLike.post_id == post_id, PostLike.user_id == user_id)))
            .scalars()
            .one_or_none()
        )

    async def add(self, db: AsyncSession, user_id: UUID, post_id: UUID, with_commit=False):
        db.add(PostLike(user_id=user_id, post_id=post_id))
        await db.flush()

        if with_commit:
            await db.commit()

    async def delete(self, db: AsyncSession, user_id: UUID, post_id: UUID, with_commit=False):
        post = await self.getByIds(db, user_id, post_id)
        await db.delete(post)
        await db.flush()

        if with_commit:
            await db.commit()
