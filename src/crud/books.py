from uuid import UUID

from sqlalchemy import String, and_, cast, distinct, func, select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import concat

from src.crud.base import CRUD
from src.model.books import Author, Book, Book_Author, Book_Genre, Genre
from src.schemas.books import BookListFilter
from src.utils.common_queries import build_json_agg_subquery, build_jsonb_filter
from src.utils.const import GenreEnum

def build_genres(query):
    query_alias = query.alias(name="main_query")
    initial_requirements_query = (  # noqa: ECE001
        select(
            query_alias.c.guid,
            func.json_agg(tuple_(Genre.guid, Genre.name)).label("genres"),
        )
        .join(Book_Genre, Book_Genre.book_id == query_alias.c.guid
        ).join(Genre, Genre.guid == Book_Genre.genre_id
        )
        .group_by(query_alias.c.guid)
    )
    return initial_requirements_query

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

    def get_filtered(self, book_filter: BookListFilter, author_name: str | None):
        query_filter = True
        
        if author_name:
            author_name_filter = cast(concat(Author.surname, " ", Author.name, " ", Author.patronymic), String).ilike(f"%{author_name}%")
            query_filter = and_(query_filter, author_name_filter)
            
        query = book_filter.filter(
            select(
                Book.guid,
                Book.title,
                Book.description,
                func.json_agg(distinct(Genre.name)).label("genres"),
                func.json_agg(distinct(concat(Author.surname, " ", Author.name, " ", Author.patronymic))).label("authors"),
                Book.rating,
                Book.pic_file_name,
                Book.isbn,
            )
            .filter(query_filter)
            .join(Book_Genre, Book_Genre.book_id == Book.guid)
            .join(Genre, Genre.guid == Book_Genre.genre_id)
            .join(Book_Author, Book_Author.book_id == Book.guid)
            .join(Author, Book_Author.author_id == Author.guid)
            .group_by(
                Book.guid,
            )
        )
        if book_filter.order_by:
            query = book_filter.sort(query)

        return query


class DBAuthor(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Author | None:
        result = await db.execute(select(Author).filter(Author.guid == guid))
        return result.scalars().one_or_none()

    async def get_all(self, db: AsyncSession) -> list[Author]:
        result = await db.execute(select(Author).order_by(Author.surname))
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
