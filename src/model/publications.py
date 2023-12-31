import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy_utils import UUIDType

from src.database import Base
from src.utils.const import PostTypeEnum


class Post(Base):
    __tablename__ = "posts"
    guid = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    type = Column(Enum(PostTypeEnum), comment="Тип поста")
    title = Column(String, comment="Название поста")
    content = Column(String, comment="Текст поста")
    image = Column(String, comment="Путь до изображения")
    book_id = Column(UUIDType(binary=False), default=uuid.uuid4)
    book_rating = Column(Float, comment="Рейтинг книги")
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())


class PostComment(Base):
    __tablename__ = "comments"
    guid = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    comment = Column(String, comment="Текст комментария")
    user_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    post_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow())


class PostLike(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    post_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
