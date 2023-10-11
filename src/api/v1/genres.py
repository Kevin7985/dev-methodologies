from fastapi import APIRouter

from src.api.dependency import DB
from src.crud.books import DBGenre
from src.schemas.books import Genre

crud_genres = DBGenre()

router = APIRouter(prefix="/genres", tags=["genres"], responses={404: {"description": "Not found"}})

@router.get("/all", summary="Список всех жанров", response_model=list[Genre])
async def get_genres(db: DB):
    return await crud_genres.get_all(db)