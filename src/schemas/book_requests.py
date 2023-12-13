from datetime import datetime
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel

from src.model.book_requests import BookRequest as m_BookRequest
from src.schemas.books import Book
from src.utils.const import BookRequestStatusEnum


class Publisher(BaseModel):
    guid: UUID
    name: str
    avatar: str | None
    login: str


class BookRequestBase(BaseModel):
    book_id: UUID
    point_id: UUID
    status: BookRequestStatusEnum


class BookRequest(BaseModel):
    guid: UUID
    created_at: datetime
    point_id: UUID
    status: BookRequestStatusEnum
    user: Publisher
    book: Book

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
        allow_population_by_field_name = True
