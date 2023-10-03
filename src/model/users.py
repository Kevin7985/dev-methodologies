import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import validates
from sqlalchemy_utils import UUIDType

from src.database import Base


class User(Base):
    __tablename__ = "users"
    guid = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    nickname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    password = Column(String, nullable=False)
    account_status = Column(String, nullable=False)
    about = Column(String)
    avatar = Column(String)

    @validates("email")
    def email_validation(self, key, email):
        # TODO: написать код
        pass

    @validates("password")
    def password_validation(self, key, password):
        # TODO: написать код
        pass
