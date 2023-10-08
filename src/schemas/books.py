from datetime import datetime
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field

from src.model.books import Book as m_Book


class Book(BaseModel):
    guid: UUID
    name: str | None
    authors: list[UUID] | None
    authors_names: list[str] | None
    publication_date: datetime | None
    rating: float | None
    quantity: int | None
    cover: str | None
    isbn: str | None
    genre: list[str] | None

    class Config:
        orm_mode = True


class BookListFilter(Filter):
    guid__in: list[UUID] | None = Field(alias="guids")
    order_by: list[str] | None
    name__ilike: str | None = Field(alias="book_title")

    class Constants(Filter.Constants):
        model = m_Book

    class Config:
        allow_population_by_field_name = True


class Author(BaseModel):
    guid: UUID
    name: str | None
    last_name: str | None
    patronymic: str | None

    class Config:
        orm_mode = True
