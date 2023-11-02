from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.users import User


class DBUser(CRUD):
    async def get(self, db: AsyncSession, guid: UUID):
        result = await db.execute(select(User).where(User.guid == guid))
        return result.scalars().one_or_none()

    async def findByParam(self, db: AsyncSession, field: str, val: str) -> User:
        result = await db.execute(select(User).where(User.__dict__[field] == val))
        return result.scalars().one_or_none()

    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.flush()
        await db.commit()
        return user

    async def update(self, db: AsyncSession, user: User, isPasswordUpdate=False) -> User:
        obj = user.dict()

        if not isPasswordUpdate:
            del obj["password"]
        else:
            obj = {"password": obj["password"]}

        update_query = sql_update(User.__table__).where(User.guid == user.guid).values(**(obj))

        await db.execute(update_query)
        await db.flush()
        await db.commit()

        return await self.get(db, user.guid)

    async def delete(self, db: AsyncSession, guid: UUID):
        user = await self.get(db, guid)
        await db.delete(user)
        await db.flush()
        await db.commit()
