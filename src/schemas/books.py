from datetime import datetime
from typing import Any
from uuid import UUID
from fastapi_filter import FilterDepends

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field

from src.model.books import Book as m_Book, Genre


class Book(BaseModel):
    guid: UUID
    title: str | None
    authors: list[str] | None
    rating: float | None
    pic_file_name: str | None
    description: str | None
    isbn: str | None
    genres: list[str] | None | Any

    class Config:
        orm_mode = True


class GenreFilter(Filter):
    guid__in: list[UUID] | None = Field(alias="genre_guids")

    class Constants(Filter.Constants):
        model = Genre

    class Config:
        allow_population_by_field_name = True


class BookListFilter(Filter):
    guid__in: list[UUID] | None = Field(alias="guids")
    order_by: list[str] | None
    title__ilike: str | None = Field(alias="book_title")
    genres: GenreFilter = FilterDepends(GenreFilter)
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
