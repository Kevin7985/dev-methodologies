import uuid

from sqlalchemy import Column, Float, String
from sqlalchemy_utils import UUIDType

from src.database import Base


class BookcrossingPoint(Base):
    __tablename__ = "bookcrossing_points"
    guid = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False, comment="Название точки буккроссинга")
    latitude = Column(Float, nullable=False, comment="Широта")
    longitude = Column(Float, nullable=False, comment="Долгота")
    address_text = Column(String, nullable=False, comment="Адрес")
