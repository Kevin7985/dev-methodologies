from uuid import UUID

from fastapi import APIRouter, status, HTTPException, status

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.users import DBUser
from src.model.users import User as m_User
from src.schemas.users import UserIn, UserOut, UserLogin, UserLogToken

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

crud_user = DBUser()


@router.post("/auth", summary="Вход в профиль пользователя", response_model=UserLogToken)
async def auth_user(db: DB, user: UserLogin) :
    return "dsaffh"
#
#
# @router.get("/all", summary="Список всех пользователей")
# async def get_all(db: DB, credentials: Credentials):
#     return "hello"


@router.post("/register", summary="Регистрация нового пользователя", status_code=status.HTTP_201_CREATED)
async def register_user(db: DB, user: UserIn) -> UserOut:
    check_email = await crud_user.findByParam(db, "email", user.email)
    if check_email:
        raise HTTPException(409, detail="Пользователь с данной почтой уже существует")

    check_login = await crud_user.findByParam(db, "login", user.login)
    if check_login:
        raise HTTPException(409, detail="Пользватель с данным логином уже существует")

    try:
        user1 = user.dict()
        user_model = m_User(**(user1))

        createdUser = await crud_user.create(db, user_model)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), user)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить пользователя в БД")

    return createdUser


# @router.get("/{id}", summary="Получение пользователя по id", response_model=User)
# async def get_user(db: DB, id: UUID, credentials: Credentials):
#     return "ds"
#
#
# @router.put("/update", summary="Редактирование профиля пользователя")
# async def upadate_user(db: DB, credentials: Credentials):
#     return "dfs"
#
#
# @router.delete("/{id}", summary="Удаление пользователя по id")
# async def delete_user(db: DB, id: UUID, credentials: Credentials):
#     return "sdfgf"
