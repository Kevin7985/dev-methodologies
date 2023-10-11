import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy_utils import UUIDType

from src.database import Base

class Book(Base):
    __tablename__ = "bookcrossing_points"
    id = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, comment="Название точки буккроссинга")
    latitude = Column(Float, comment="Широта")
    longitude = Column(Float, comment="Долгота")