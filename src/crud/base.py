from abc import abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base


class CRUD:
    @staticmethod
    def update_row(row: type[Base], updates: dict | type[Base]):
        for key, value in (updates if isinstance(updates, dict) else vars(updates)).items():
            if key != "_sa_instance_state":
                setattr(row, key, value)
        return row

    @abstractmethod
    async def get(self, *args):
        pass

    @abstractmethod
    async def create(self, *args):
        pass

    @abstractmethod
    async def update(self, *args):
        pass

    @abstractmethod
    async def delete(self, *args):
        pass


class CRUDObject(CRUD):
    async def create(self, db: AsyncSession, created_obj, with_commit=False):
        db.add(created_obj)
        await db.flush()

        if with_commit:
            await db.commit()
            
        return created_obj

    async def get(self, db: AsyncSession, obj):
        obj_class = type(obj)
        guid = obj.guid
        result = await db.execute(select(obj_class).filter(obj_class.guid == str(guid)))
        return result.scalars().first()

    async def get_by_id(self, db: AsyncSession, guid: str, obj_class):
        result = await db.execute(select(obj_class).filter(obj_class.guid == str(guid)))
        return result.scalars().first()

    @staticmethod
    async def get_many(db: AsyncSession, obj_class, guids=None):
        result = await db.execute(select(obj_class))
        if guids and isinstance(guids, list | tuple):
            result = await db.execute(select(obj_class).filter(obj_class.guid.in_(guids)))
        return result.scalars().all()

    async def update(self, db: AsyncSession, exist_obj, new_obj):
        self.update_row(row=exist_obj, updates=new_obj)
        await db.flush()
        await db.commit()
        return exist_obj

    async def delete(self, db: AsyncSession, obj) -> None:
        await db.delete(obj)
        await db.commit()
