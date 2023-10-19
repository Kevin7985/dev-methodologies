from uuid import UUID

from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field

from src.model.books import Book as m_Book
from src.model.books import Genre as m_Genre


class Author(BaseModel):
    guid: UUID
    name: str | None
    surname: str | None
    patronymic: str | None

    class Config:
        orm_mode = True


class Genre(BaseModel):
    guid: UUID
    name: str | None


class BookBase(BaseModel):
    title: str
    pic_file_name: str | None
    description: str | None
    isbn: str | None


class BookOut(BookBase):
    guid: UUID
    authors: list[Author] | None
    rating: float | None
    genres: list[Genre] | None

    class Config:
        orm_mode = True


class BookIn(BookBase):
    authors: list[UUID]
    genres: list[UUID]


class Book(BaseModel):
    guid: UUID
    title: str
    pic_file_name: str | None
    description: str | None
    isbn: str | None
    rating: float | None


class GenreFilter(Filter):
    guid__in: list[UUID] | None = Field(alias="genre_guids")

    class Constants(Filter.Constants):
        model = m_Genre

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
