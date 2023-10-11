import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy_utils import UUIDType

from src.database import Base

class Book(Base):
    __tablename__ = "requests"
    id = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    book_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    point_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)