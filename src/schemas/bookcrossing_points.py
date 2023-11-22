from typing import Any
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field

from src.model.bookcrossing_points import BookcrossingPoint as m_BookcrossingPoint


class BookcrossingPointBase(BaseModel):
    title: str
    latitude: float
    longitude: float
    address_text: str

class BookcrossingPoint(BookcrossingPointBase):
    guid: UUID

    class Config:
        orm_mode = True


class PointsFilter(Filter):
    title__ilike: str = Field(alias="point_title", default=None)

    class Constants(Filter.Constants):
        model = m_BookcrossingPoint

    class Config:
        allow_population_by_field_name = True

