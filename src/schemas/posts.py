from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from src.utils.const import PostTypeEnum


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
