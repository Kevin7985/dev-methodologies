import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy_utils import UUIDType

from src.database import Base


class BookRequest(Base):
    __tablename__ = "requests"
    guid = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    book_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    point_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow())
