from fastapi import APIRouter, Query

from src.api.dependency import DB
from src.crud.books import DBGenre
from src.schemas.books import Genre


router = APIRouter(prefix="/genres", tags=["genres"])
DEFAULT_LIST_GENRES = Query(default=None, description="List of genres")

crud_genres = DBGenre()

@router.get("/all", summary="Список всех жанров", response_model=list[Genre])
async def get_all(db: DB):
    return await crud_genres.get_all(db)
