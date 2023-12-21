from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.book_requests import DBBookRequest
from src.crud.bookcrossing_points import DBBookcrossingPoint
from src.crud.books import DBBook
from src.database import Redis
from src.model.book_requests import BookRequest as m_BookRequest
from src.schemas.book_requests import BookRequest, BookRequestBase, BookRequestListFilter, BookRequestUpdate
from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/book-requests", tags=["book requests"])

crud_book = DBBook()
crud_points = DBBookcrossingPoint()
crud_requests = DBBookRequest()

_CollectionOfOfferFilter = Annotated[BookRequestListFilter, FilterDepends(BookRequestListFilter)]


@router.post("/create", summary="Создание нового запроса")
async def add_book_request(credentials: Credentials, db: DB, req: BookRequestBase):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    if not (await crud_book.get(db, req.book_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная книга не найдена")

    if not (await crud_points.get(db, req.point_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная точка буккроссинга не найдена")

    try:
        req1 = req.dict()
        req_model = m_BookRequest(**(req1))
        req_model.user_id = user_id
        req_model.created_at = datetime.now()

        created_req = await crud_requests.create(db, req_model, True)
    except Exception as e:
        await log.aerror("%s @ %s", repr(e), req)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить запрос в БД")

    return created_req


@router.get("/all", summary="Получение всех запросов", response_model=Page[BookRequest])
async def get_all(credentials: Credentials, db: DB, reqFilter: _CollectionOfOfferFilter):
    await checkAuth(db, credentials.credentials)
    return await paginate(db, crud_requests.get_filtered(reqFilter), unique=False)


@router.get("/{id}", summary="Получение запроса по guid", response_model=BookRequest)
async def get_req_by_id(credentials: Credentials, db: DB, id: UUID):
    await checkAuth(db, credentials.credentials)

    if not (db_req := await crud_requests.get(db, id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный запрос не найден")

    return db_req


@router.put("/update", summary="Обновление запроса", response_model=BookRequest)
async def update_req(credentials: Credentials, db: DB, req: BookRequestUpdate):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    if not (await crud_requests.get(db, req.guid)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный запрос не найден")

    if not (await crud_book.get(db, req.book_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная книга не найдена")

    if not (await crud_points.get(db, req.point_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная точка буккроссинга не найдена")

    try:
        updated_req = await crud_requests.update(db, req, True)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось обновить запрос")

    return updated_req


@router.delete("/{id}", summary="Удаление запроса по guid")
async def delete_req(credentials: Credentials, db: DB, id: UUID):
    await checkAuth(db, credentials.credentials)

    if not (db_req := await crud_requests.get(db, id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данный запрос не найден")

    try:
        await crud_requests.delete(db, db_req, True)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить запрос")
