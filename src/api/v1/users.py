from uuid import UUID

from fastapi import APIRouter, status, HTTPException, status

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.users import DBUser
from src.model.users import User as m_User
from src.schemas.users import User, UserIn, UserOut, UserLogin, UserLogToken, UserUpdate, UserPasswordUpdate

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
    await checkAuth(db, credentials.credentials)

    user = await crud_user.get(db, id)
    if not user:
        raise HTTPException(404, detail="Пользователь с данным guid не найден")

    return  UserOut(**(user.__dict__))


@router.put("/update", summary="Редактирование профиля пользователя")
async def upadate_user(credentials: Credentials, db: DB, user: UserUpdate):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))
    if user.guid != user_id:
        raise HTTPException(403, detail="Данное действие недоступно с данным токеном")

    try:
        user_dict = user.dict()
        user_model = User(**(user_dict))

        await crud_user.update(db, user_model)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось обновить пользователя в БД")

@router.put("/change-password", summary="Смена пароля пользователя")
async def update_user_password(credentials: Credentials, db: DB, user: UserPasswordUpdate):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))
    if user.guid != user_id:
        raise HTTPException(403, detail="Данное действие недоступно с данным токеном")

    dbUser = await crud_user.get(db, user_id)
    if dbUser.password != user.oldPassword:
        raise HTTPException(403, "Неверный старый пароль")

    try:
        user_dict = user.dict()
        user_dict["password"] = user_dict["newPassword"]
        user_model = User(**(user_dict))

        await crud_user.update(db, user_model, True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось обновить пароль пользователя в БД")


@router.delete("/{id}", summary="Удаление пользователя по id", status_code=status.HTTP_200_OK)
async def delete_user(db: DB, id: UUID, credentials: Credentials):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))
    if id != user_id:
        raise HTTPException(403, detail="Данное действие недоступно с данным токеном")

    await crud_user.delete(db, id)
