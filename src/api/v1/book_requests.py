from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB, Credentials
from src.config import log
from src.database import Redis
from src.crud.books import DBBook
from src.crud.book_requests import DBBookRequest
from src.model.book_requests import BookRequest as m_BookRequest
from src.crud.bookcrossing_points import DBBookcrossingPoint
from src.schemas.book_requests import BookRequestBase, BookRequestListFilter
from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/book-requests", tags=["Book requests"])

crud_book = DBBook()
crud_points = DBBookcrossingPoint()
crud_requests = DBBookRequest()

_CollectionOfOfferFilter = Annotated[BookRequestListFilter, FilterDepends(BookRequestListFilter)]


@router.post("/create", summary="Создание нового запроса")
async def add_book_request(credentials: Credentials, db: DB, req: BookRequestBase):
    await checkAuth(db, credentials.credentials)

    user_id = UUID(Redis.get(credentials.credentials).decode("utf-8"))

    if not (db_book := await crud_book.get(db, req.book_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная книга не найдена")

    if not (db_point := await crud_points.get(db, req.point_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная точка букроссинга не найдена")

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
