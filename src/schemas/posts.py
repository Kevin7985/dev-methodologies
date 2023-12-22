from datetime import datetime
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel

from src.model.publications import Post as m_Post
from src.schemas.book_requests import Publisher
from src.schemas.books import Book
from src.utils.const import PostTypeEnum


class PostBase(BaseModel):
    book_id: UUID | None
    type: PostTypeEnum
    title: str | None
    content: str | None
    image: str | None
    book_rating: float | None = 0


class Post(PostBase):
    guid: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostAllInfo(BaseModel):
    guid: UUID
    created_at: datetime
    updated_at: datetime
    user: Publisher
    book: Book | None
    book_rating: float | None
    type: PostTypeEnum
    title: str | None
    content: str | None
    image: str | None

    class Config:
        orm_mode = True


class PostListFilter(Filter):
    user_id: UUID | None
    book_id: UUID | None
    type: PostTypeEnum | None

    class Constants(Filter.Constants):
        model = m_Post

    class Config:
        allow_population_by_field_name = True


class PostCommentBase(BaseModel):
    comment: str
    user_id: UUID
    post_id: UUID


class PostCommentIn(BaseModel):
    comment: str


class PostCommentUpdate(BaseModel):
    guid: UUID
    comment: str


class PostComment(PostCommentBase):
    guid: UUID
    created_at: datetime

    class Config:
        orm_mode = True
