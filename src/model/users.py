import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from sqlalchemy_utils import UUIDType

from src.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUIDType(binary=False), nullable=False, unique=True, primary_key=True, index=True, default=uuid.uuid4)
    login = Column(String, nullable=False, comment="Логин пользователя")
    name = Column(String, comment="Имя пользователя")
    about = Column(String, comment="Описание пользователя")
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, comment="Телефон пользователя")
    avatar = Column(String, comment="Аватар пользователя")

    @validates("email")
    def email_validation(self, key, email):
        # TODO: написать код
        pass

    @validates("password")
    def password_validation(self, key, password):
        # TODO: написать код
        pass
