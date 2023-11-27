from uuid import UUID
from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel

from src.utils.const import PostTypeEnum
from src.model.publications import Post as m_Post


class PostBase(BaseModel):
    book_id: UUID
    type: PostTypeEnum
    title: str | None
    content: str | None
    image: str | None
    book_rating: float = 0


class Post(PostBase):
    guid: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostListFilter(Filter):
    user_id: UUID | None
    book_id: UUID | None
    type: PostTypeEnum | None

    class Constants(Filter.Constants):
        model=m_Post

    class Config:
        allow_population_by_field_name=True


class PostCommentBase(BaseModel):
    comment: str
    user_id: UUID
    post_id: UUID


class PostCommentIn(BaseModel):
    comment: str


class PostComment(PostCommentBase):
    guid: UUID
    created_at: datetime
