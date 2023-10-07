from uuid import UUID

from sqlalchemy import and_, case, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.books import Author, Book
from src.schemas.books import BookListFilter
from src.utils.common_queries import build_json_agg_subquery, build_jsonb_filter
from src.utils.const import GenreEnum


class DBBook(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Book | None:
        result = await db.execute(select(Book).filter(Book.guid == guid))
        return result.scalars().one_or_none()

    async def get_all(self, db: AsyncSession) -> list[Book]:
        result = await db.execute(select(Book))
        return result.scalars().all()

    async def create(self, db: AsyncSession, Book: Book) -> Book:
        db.add(Book)
        await db.flush()
        await db.commit()
        return Book

    async def update(self, *args):
        pass

    async def delete(self, *args):
        pass

    async def get_filtered(self, book_filter: BookListFilter, genre: list[GenreEnum] | None, authors: list[UUID] | None):
        query_filter = True
        if genre:
            genre_filter = build_jsonb_filter(jsonb_column=Book.genre, sought_values=genre)
            query_filter = and_(query_filter, genre_filter)
        if authors:
            authors_filter = build_jsonb_filter(jsonb_column=Book.authors, sought_values=authors)
            query_filter = and_(query_filter, authors_filter)
            authors_names = build_json_agg_subquery(jsonb_column=Book.authors, joined_model=Author, agg_column=Author.name)
        query = book_filter.filter(
            select(
                Book.guid,
                Book.name,
                Book.authors,
                (authors_names).label("authors_names"),
                Book.publication_date,
                Book.rating,
                Book.quantity,
                Book.cover,
                Book.isbn,
            )
            .filter(query_filter)
            )
        return query