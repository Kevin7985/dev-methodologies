from uuid import UUID

from sqlalchemy import String, and_, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import concat

from src.crud.base import CRUD
from src.model.books import Author, Book, Book_Author, Book_Genre, Genre
from src.schemas.books import BookListFilter


def build_genres(query):
    query_alias = query.alias(name="main_query")
    initial_requirements_query = (  # noqa: ECE001
        select(query_alias.c.guid, func.json_agg(Genre.guid).label("genres"))
        .select_from(query_alias)
        .join(Book_Genre, Book_Genre.book_id == query_alias.c.guid)
        .join(Genre, Genre.guid == Book_Genre.genre_id)
        .group_by(query_alias.c.guid)
    )
    print(initial_requirements_query)
    return initial_requirements_query


def build_authors(query):
    query_alias = query.alias(name="main_query")
    initial_requirements_query = (  # noqa: ECE001
        select(
            query_alias.c.guid,
            func.json_agg(concat(Author.surname, " ", Author.name, " ", Author.patronymic)).label("authors"),
        )
        .select_from(query_alias)
        .join(Book_Author, Book_Author.book_id == query_alias.c.guid)
        .join(Author, Book_Author.author_id == Author.guid)
        .group_by(query_alias.c.guid)
    )
    return initial_requirements_query


class DBBook(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Book | None:
        authors = (await db.execute(select(Author).join(Book_Author, Book_Author.book_id == guid).filter(Author.guid == Book_Author.author_id))).scalars().all()
        genres = (await db.execute(select(Genre).join(Book_Genre, Book_Genre.book_id == guid).filter(Genre.guid == Book_Genre.genre_id))).scalars().all()
        book = (await db.execute(select(Book).filter(Book.guid == guid))).scalars().one_or_none()

        book.authors = authors
        book.genres = genres
        return book

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

    async def delete(self, db: AsyncSession, guid: UUID) -> bool:
        Book = await self.get(db, guid)
        if not Book:
            return False

        await db.delete(Book)
        await db.flush()
        await db.commit()
        return True

    async def get_books_filtered(self, db: AsyncSession, book_filter: BookListFilter):
        print(book_filter)
        if not book_filter.genres.guid__in:
            books_genres = (await db.execute(select(Book_Genre.book_id))).scalars().all()
        else:
            books_genres = (await db.execute(select(Book_Genre.book_id).filter(Book_Genre.genre_id.in_(book_filter.genres.guid__in)))).scalars().all()


        if book_filter.author__ilike:
            author_name_filter = cast(concat(Author.surname, " ", Author.name, " ", Author.patronymic), String).ilike(
                f"%{book_filter.author__ilike}%"
            )

            authors = (await db.execute(select(Author.guid).filter(author_name_filter))).scalars().all()
        else:
            authors = (await db.execute(select(Author.guid))).scalars().all()

        books_authors = (await db.execute(select(Book_Author.book_id).filter(Book_Author.author_id.in_(authors)))).scalars().all()
        
        if book_filter.title__ilike:
            books_titles = (await db.execute(select(Book.guid).filter(Book.title.ilike(f'%{book_filter.title__ilike}%')))).scalars().all()
        else:
            books_titles = (await db.execute(select(Book.guid))).scalars().all()

        filters = and_(
            Book.guid.in_(books_genres),
            Book.guid.in_(books_authors),
            Book.guid.in_(books_titles)
        )

        books = select(Book).filter(filters)

        res = (await db.execute(books)).scalars().all()
        out = []
        for item in res:
            out.append(await self.get(db, item.guid))
        
        return out

    # def get_filtered(self, book_filter: BookListFilter, author_name: str | None):
    #     print(author_name)
    #     query_filter = True

    #     if author_name:
    #         author_name_filter = cast(concat(Author.surname, " ", Author.name, " ", Author.patronymic), String).ilike(
    #             f"%{author_name}%"
    #         )

    #         query_filter = and_(query_filter, author_name_filter)

    #     query = book_filter.filter(  # noqa: ECE001
    #         select(Book.guid, Book.title, Book.description, Book.rating, Book.pic_file_name, Book.isbn)
    #         .filter(query_filter)
    #         .join(Book_Genre, Book_Genre.book_id == Book.guid)
    #         .join(Genre, Genre.guid == Book_Genre.genre_id)
    #         .join(Book_Author, Book_Author.book_id == Book.guid)
    #         .join(Author, Book_Author.author_id == Author.guid)
    #         .group_by(Book.guid)
    #     )
    #     if book_filter.order_by:
    #         query = book_filter.sort(query)

    #     query_alias = query.alias(name="main_query")

    #     genres_query = build_genres(query_alias)
    #     genres_query_alias = genres_query.alias(name="genres_query")
    #     authors_query = build_authors(query_alias)
    #     authors_query_alias = authors_query.alias(name="authors_query")
    #     query = (
    #         select(query_alias, genres_query_alias.c.genres, authors_query_alias.c.authors)
    #         .join(genres_query_alias, genres_query_alias.c.guid == query_alias.c.guid)
    #         .join(authors_query_alias, authors_query_alias.c.guid == query_alias.c.guid)
    #     )

    #     print(query)

    #     return query


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


class DBGenre(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> Genre | None:
        result = await db.execute(select(Genre).filter(Genre.guid == guid))
        return result.scalars().one_or_none()

    async def get_all(self, db: AsyncSession) -> list[Genre]:
        result = await db.execute(select(Genre))
        return result.scalars().all()