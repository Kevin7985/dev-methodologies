import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import UUIDType

from src.database import Base


class Book(Base):
    __tablename__ = "books"
    guid = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, comment="Название книги")
    authors = Column(JSONB, comment="Список авторов")
    status = Column(UUIDType(binary=False), comment="Статус книги")
    publication_date = Column(DateTime, comment="Дата публикации")
    rating = Column(Float, comment="Оценка пользователей")
    quantity = Column(Integer, default=0, comment="Количество экземпляров")
    cover = Column(String, comment="Обложка книги")
    isbn = Column(String, comment="ISBN - книги")


class Author(Base):
    __tablename__ = "authors"
    guid = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, comment="Имя")
    last_name = Column(String, comment="Фамилия")
    patronymic = Column(String, comment="Отчество")
