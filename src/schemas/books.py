from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from src.model.books import Book as m_Book
from fastapi_filter.contrib.sqlalchemy import Filter

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

    class Config:
        orm_mode = True


class BookListFilter(Filter):
    guid__in: list[UUID] | None = Field(alias="guid")
    name__ilike: str | None = Field(alias="name")
    
    class Constants(Filter.Constants):
        model = m_Book

    class Config:
        allow_population_by_field_name = True