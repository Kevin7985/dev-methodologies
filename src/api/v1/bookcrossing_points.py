from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependency import DB, Credentials
from src.config import log
from src.crud.bookcrossing_points import DBBookcrossingPoint, build_all_points
from src.model.bookcrossing_points import BookcrossingPoint as m_BookcrossingPoint
from src.schemas.bookcrossing_points import BookcrossingPoint, BookcrossingPointBase, PointsFilter
from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/bookcrossing-points", tags=["bookcrossing-points"])

crud_points = DBBookcrossingPoint()
_BookcrossingPointsFilter = Annotated[PointsFilter, FilterDepends(PointsFilter)]


@router.get("/all", summary="Список точек буккроссинга", response_model=Page[BookcrossingPoint])
async def get_all(db: DB, credentials: Credentials, points_filter: _BookcrossingPointsFilter):
    await checkAuth(db, credentials.credentials)
    return await paginate(db, build_all_points(points_filter=points_filter))


@router.post("/create", summary="Создание точки буккросинга")
async def create_point(db: DB, credentials: Credentials, point: BookcrossingPointBase):
    await checkAuth(db, credentials.credentials)
    try:
        point_model = m_BookcrossingPoint(**(point.dict()))
        created_point = await crud_points.create(db, point_model, with_commit=True)
    except Exception as e:
        await log.aerror("%s", repr(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить запись в БД")
    return created_point
