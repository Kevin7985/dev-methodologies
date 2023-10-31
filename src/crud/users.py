from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.users import User

class DBUser(CRUD):
    async def findByParam(self, db: AsyncSession, field: str, val: str) -> User:
        result = await db.execute(select(User).where(User.__dict__[field] == val))
        return result.scalars().one_or_none()


    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.flush()
        await db.commit()
        return user
