from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Book(BaseModel):
    guid: UUID
    name: str | None
    authors: list[UUID] | None
    status: str | None
    publication_date: datetime | None
    rating: float | None
    quantity: int | None
    cover: str | None
    isbn: str | None

    class Config:
        orm_mode = True
