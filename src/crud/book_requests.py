from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUD
from src.model.book_requests import BookRequest
from src.model.bookcrossing_points import BookcrossingPoint
from src.model.books import Book
from src.model.users import User
from src.schemas.book_requests import BookRequest as BookRequest_s
from src.schemas.book_requests import BookRequestListFilter


def build_book_request_query():
    query = (
        select(
            BookRequest.guid,
            BookRequest.created_at,
            BookRequest.status,
            func.json_build_object(
                "guid",
                Book.guid,
                "title",
                Book.title,
                "pic_file_name",
                Book.pic_file_name,
                "description",
                Book.description,
                "isbn",
                Book.isbn,
                "rating",
                Book.rating,
            ).label("book"),
            func.json_build_object(
                "guid", User.guid, "name", User.name, "avatar", User.avatar, "login", User.login
            ).label("user"),
            func.json_build_object(
                "guid",
                BookcrossingPoint.guid,
                "title",
                BookcrossingPoint.title,
                "address_text",
                BookcrossingPoint.address_text,
            ).label("point"),
        )
        .join(User, User.guid == BookRequest.user_id)
        .join(Book, Book.guid == BookRequest.book_id)
        .join(BookcrossingPoint, BookcrossingPoint.guid == BookRequest.point_id)
    )
    return query


class DBBookRequest(CRUD):
    async def get(self, db: AsyncSession, guid: UUID) -> BookRequest_s | None:
        return (await db.execute((build_book_request_query()).where(BookRequest.guid == guid))).mappings().one_or_none()

    async def create(self, db: AsyncSession, req: BookRequest, with_commit=False) -> BookRequest_s:
        db.add(req)
        await db.flush()

        if with_commit:
            await db.commit()

        return await self.get(db, req.guid)

    async def update(self, db: AsyncSession, req: BookRequest, with_commit=False):
        update_query = (
            sql_update(BookRequest.__table__)
            .where(BookRequest.guid == req.guid)
            .values({"book_id": req.book_id, "point_id": req.point_id, "status": req.status})
        )

        await db.execute(update_query)
        await db.flush()

        if with_commit:
            await db.commit()

        return await self.get(db, req.guid)

    async def delete(self, db: AsyncSession, req: BookRequest, with_commit=False):
        await db.delete(req)

        if with_commit:
            await db.commit()

    def get_filtered(self, req_filter: BookRequestListFilter):
        query = req_filter.filter(build_book_request_query())

        return query
