from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.bookcrossing_points import BookcrossingPoint
from src.schemas.bookcrossing_points import PointsFilter
from src.utils.exceptions import validate_coordinates_or_fail


def build_all_points(points_filter: PointsFilter) -> Select[Any]:
    query = select(BookcrossingPoint)
    if points_filter.title__ilike:
        query = points_filter.filter(query)
    return query


class DBBookcrossingPoint(CRUD):
    async def get_all(self, db: AsyncSession, points_filter: PointsFilter) -> list[BookcrossingPoint]:
        query = build_all_points(points_filter=points_filter)
        return (await db.execute(query)).scalars().all()

    async def create(self, db: AsyncSession, created_obj, with_commit=False) -> BookcrossingPoint:
        validate_coordinates_or_fail(created_obj)
        db.add(created_obj)
        await db.flush()

        if with_commit:
            await db.commit()

        return created_obj
