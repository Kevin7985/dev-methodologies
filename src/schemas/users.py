from uuid import UUID

from pydantic import BaseModel

class UserBase(BaseModel):
    login: str | None
    name: str | None
    about: str | None
    email: str | None
    password: str | None
    avatar: str | None


class User(BaseModel):
    guid: UUID
    login: str | None
    name: str | None
    about: str | None
    email: str | None
    password: str | None
    avatar: str | None

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    login: str | None
    name: str | None
    email: str | None
    password: str | None


class UserOut(BaseModel):
    guid: UUID
    login: str | None
    name: str | None
    about: str | None
    email: str | None
    avatar: str | None

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    login: str | None
    password: str |None


class UserLog(UserOut):
    access_token: str | None


class UserUpdate(BaseModel):
    guid: UUID
    login: str | None
    name: str | None
    about: str | None
    email: str | None
    avatar: str | None


class UserPasswordUpdate(BaseModel):
    guid: UUID
    oldPassword: str | None
    newPassword: str | None
