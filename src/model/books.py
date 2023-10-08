import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import UUIDType

from src.database import Base


class Book(Base):
    __tablename__ = "books"
    book_id = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, comment="Название книги")
    description = Column(String, comment="Описание книги")
    rating = Column(Float, comment="Оценка пользователей")
    isbn = Column(String, comment="IBSN книги")
    pic_file_name = Column(String, comment="Обложка книги")


class Author(Base):
    __tablename__ = "authors"
    author_id = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, comment="Имя автора")
    surname = Column(String, comment="Фамилия автора")
    patronymic = Column(String, comment="Отчество автора")


class Genre(Base):
    __tablename__ = "genres"
    genre_id = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, comment="Название жанра")


class Book_Author(Base):
    __tablename__ = "book_author"
    book_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    author_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)


class Book_Genre(Base):
    __tablename__ = "book_genre"
    book_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    genre_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)