from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from fastapi_filter.contrib.sqlalchemy import Filter

from src.model.book_requests import BookRequest as m_BookRequest
from src.utils.const import BookRequestStatusEnum


class BookRequestBase(BaseModel):
    book_id: UUID
    point_id: UUID
    status: BookRequestStatusEnum


class BookRequest(BookRequestBase):
    guid: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class BookRequestUpdate(BaseModel):
    guid: UUID | None
    book_id: UUID | None
    point_id: UUID | None
    status: BookRequestStatusEnum | None

    class Config:
        orm_mode = True


class BookRequestListFilter(Filter):
    user_id: UUID | None
    book_id: UUID | None
    point_id: UUID | None
    status: BookRequestStatusEnum | None

    class Constants(Filter.Constants):
        model = m_BookRequest

    class Config:
        allow_population_by_field_name=True
