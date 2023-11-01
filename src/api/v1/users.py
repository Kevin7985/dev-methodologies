from uuid import UUID

from fastapi import APIRouter, status, HTTPException, status

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.users import DBUser
from src.model.users import User as m_User
from src.schemas.users import UserIn, UserOut, UserLogin, UserLogToken

from src.database import Redis
from src.utils.funcs import generateToken

from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

crud_user = DBUser()


@router.post("/auth", summary="Вход в профиль пользователя", response_model=UserLogToken)
async def auth_user(db: DB, user: UserLogin):
    check_email = await crud_user.findByParam(db, "email", user.login)
    check_login = await crud_user.findByParam(db, "login", user.login)

    if (not check_email) and (not check_login):
        raise HTTPException(404, detail="Неверный логин или пароль")

    dbUser = None
    if check_email:
        dbUser = check_email
    else:
        dbUser = check_login

    if user.password != dbUser.password:
        raise HTTPException(404, detail="Неверный логин или пароль")

    auth_token = generateToken()

    Redis.set(auth_token, str(dbUser.guid))
    Redis.expire(auth_token, 24 * 3600)

    return UserLogToken(access_token=auth_token)


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


@router.get("/{id}", summary="Получение пользователя по id", response_model=UserOut)
async def get_user(db: DB, id: UUID, credentials: Credentials):
    checkAuth(credentials.credentials)

    user = await crud_user.get(db, id)
    if not user:
        raise HTTPException(404, detail="Пользователь с данным guid не найден")

    return  UserOut(**(user.__dict__))
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
