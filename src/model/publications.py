import uuid

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import UUIDType

from src.database import Base
from src.utils.const import PostTypeEnum

class Post(Base):
    __tablename__ = "posts"
    id = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    type = Column(PostTypeEnum.db_type(), comment="Тип поста")
    title = Column(String, comment="Название поста")
    content = Column(String, comment="Текст поста")
    image = Column(String, comment="Путь до изображения")
    book_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    book_rating = Column(Float, comment="Рейтинг книги")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class PostComments(Base):
    __tablename__ = "comments"
    id = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    comment = Column(String, comment="Текст комментария")
    user_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    post_id = Column(UUIDType(binary=False), nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)