from uuid import UUID

from sqlalchemy import String, and_, cast, func, select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import concat

from src.crud.base import CRUD
from src.model.books import Author, Book, Book_Author, Book_Genre, Genre
from src.schemas.books import BookListFilter


def build_genres(query):
    query_alias = query.alias(name="main_query")
    initial_requirements_query = (  # noqa: ECE001
        select(
            query_alias.c.guid,
            func.json_agg(func.json_build_object("guid", Genre.guid, "name", Genre.name)).label("genres"),
        )
        .select_from(query_alias)
        .join(Book_Genre, Book_Genre.book_id == query_alias.c.guid)
        .join(Genre, Genre.guid == Book_Genre.genre_id)
        .group_by(query_alias.c.guid)
    )
    return initial_requirements_query


def build_authors(query):
    query_alias = query.alias(name="main_query")
    initial_requirements_query = (  # noqa: ECE001
        select(
            query_alias.c.guid,
            func.json_agg(
                func.json_build_object(
                    "guid", Author.guid, "name", Author.name, "surname", Author.surname, "patronymic", Author.patronymic
                )
            ).label("authors"),
        )
        .select_from(query_alias)
        .join(Book_Author, Book_Author.book_id == query_alias.c.guid)
        .join(Author, Book_Author.author_id == Author.guid)
        .group_by(query_alias.c.guid)
    )
    return initial_requirements_query


class DBBook(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Book | None:
        authors = (
            (
                await db.execute(
                    select(Author)
                    .join(Book_Author, Book_Author.book_id == guid)
                    .filter(Author.guid == Book_Author.author_id)
                )
            )
            .scalars()
            .all()
        )
        genres = (
            (
                await db.execute(
                    select(Genre).join(Book_Genre, Book_Genre.book_id == guid).filter(Genre.guid == Book_Genre.genre_id)
                )
            )
            .scalars()
            .all()
        )
        book = (await db.execute(select(Book).filter(Book.guid == guid))).scalars().one_or_none()

        if not book:
            return book

        book.authors = authors
        book.genres = genres
        return book

    async def get_all(self, db: AsyncSession) -> list[Book]:
        result = await db.execute(select(Book))
        return result.scalars().all()

    async def create(self, db: AsyncSession, book: Book, with_commit=False) -> Book:
        db.add(book)
        await db.flush()

        if with_commit:
            await db.commit()

        return await self.get(db, book.guid)

    async def update(self, db: AsyncSession, obj: Book, with_commit=False):
        update_query = sql_update(Book.__table__).where(Book.guid == obj.guid).values(**(obj.dict()))

        await db.execute(update_query)
        await db.flush()

        if with_commit:
            await db.commit()

        return await self.get(db, obj.guid)

    async def delete(self, db: AsyncSession, obj: Book, with_commit=False):
        await db.delete(obj)

        if with_commit:
            await db.commit()

    def get_filtered(self, book_filter: BookListFilter, author_name: str | None):
        query_filter = True

        if author_name:
            author_name_filter = cast(concat(Author.surname, " ", Author.name, " ", Author.patronymic), String).ilike(
                f"%{author_name}%"
            )
            query_filter = and_(query_filter, author_name_filter)

        query = book_filter.filter(  # noqa: ECE001
            select(Book.guid, Book.title, Book.description, Book.rating, Book.pic_file_name, Book.isbn)
            .filter(query_filter)
            .join(Book_Genre, Book_Genre.book_id == Book.guid)
            .join(Genre, Genre.guid == Book_Genre.genre_id)
            .join(Book_Author, Book_Author.book_id == Book.guid)
            .join(Author, Book_Author.author_id == Author.guid)
            .group_by(Book.guid)
        )
        if book_filter.order_by:
            query = book_filter.sort(query)

        query_alias = query.alias(name="main_query")

        genres_query = build_genres(query_alias)
        genres_query_alias = genres_query.alias(name="genres_query")
        authors_query = build_authors(query_alias)
        authors_query_alias = authors_query.alias(name="authors_query")
        query = (
            select(query_alias, genres_query_alias.c.genres, authors_query_alias.c.authors)
            .join(genres_query_alias, genres_query_alias.c.guid == query_alias.c.guid)
            .join(authors_query_alias, authors_query_alias.c.guid == query_alias.c.guid)
        )

        return query


class DBAuthor(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Author | None:
        result = await db.execute(select(Author).filter(Author.guid == guid))
        return result.scalars().one_or_none()

    def get_all(self, author_name: str | None):
        query = select(Author).order_by(Author.surname)
        if author_name:
            query = query.filter(
                cast(concat(Author.surname, " ", Author.name, " ", Author.patronymic), String).ilike(f"%{author_name}%")
            )
        return query

    async def get_many(self, db: AsyncSession, guids: list[UUID]) -> list[Author]:
        result = await db.execute(select(Author).filter(Author.guid.in_(guids)))
        return result.scalars().all()

    async def create(self, db: AsyncSession, author: Author) -> Author:
        db.add(author)
        await db.flush()
        await db.commit()
        return author

    async def update(self, *args):
        pass

    async def delete(self, *args):
        pass


class DBGenre(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Genre | None:
        result = await db.execute(select(Genre).filter(Genre.guid == guid))
        return result.scalars().one_or_none()

    async def get_all(self, db: AsyncSession) -> list[Genre]:
        result = await db.execute(select(Genre).order_by(Genre.name))
        return result.scalars().all()

    async def get_many(self, db: AsyncSession, guids: list[UUID]) -> list[Genre]:
        result = await db.execute(select(Genre).filter(Genre.guid.in_(guids)))
        return result.scalars().all()

    async def create(self, db: AsyncSession, genre: Genre) -> Genre:
        db.add(genre)
        await db.flush()
        await db.commit()
        return genre

    async def update(self, *args):
        pass

    async def delete(self, *args):
        pass


class DBBookAuthor(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Book_Author | None:
        pass

    async def get_all(self, db: AsyncSession) -> list[Book_Author]:
        result = await db.execute(select(Book_Author))
        return result.scalars().all()

    async def get_by_book(self, db: AsyncSession, book_guid: UUID) -> list[Book_Author]:
        result = await db.execute(select(Book_Author).filter(Book_Author.book_id == book_guid))
        return result.scalars().all()

    async def update(self, *args):
        pass

    async def delete(self, db: AsyncSession, obj: Book_Author, with_commit=False):
        await db.delete(obj)

        if with_commit:
            await db.commit()

    async def delete_by_book(self, db: AsyncSession, book_guid: UUID, with_commit=False):
        objects = await self.get_by_book(db, book_guid)
        for obj in objects:
            await self.delete(db, obj, with_commit)


class DBBookGenre(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Book_Genre | None:
        pass

    async def get_all(self, db: AsyncSession) -> list[Book_Genre]:
        result = await db.execute(select(Book_Genre))
        return result.scalars().all()

    async def get_by_book(self, db: AsyncSession, book_guid: UUID) -> list[Book_Genre]:
        result = await db.execute(select(Book_Genre).filter(Book_Genre.book_id == book_guid))
        return result.scalars().all()

    async def update(self, *args):
        pass

    async def delete(self, db: AsyncSession, obj: Book_Genre, with_commit=False):
        await db.delete(obj)

        if with_commit:
            await db.commit()

    async def delete_by_book(self, db: AsyncSession, book_guid: UUID, with_commit=False):
        objects = await self.get_by_book(db, book_guid)
        for obj in objects:
            await self.delete(db, obj, with_commit)
