from fastapi import APIRouter, HTTPException, Query, status

from src.api.dependency import DB
from src.crud.books import DBGenre
from src.model.books import Genre as m_genre
from src.schemas.books import Genre, GenreBase

router = APIRouter(prefix="/genres", tags=["genres"])
DEFAULT_LIST_GENRES = Query(default=None, description="List of genres")

crud_genres = DBGenre()


@router.get("/all", summary="Список всех жанров", response_model=list[Genre])
async def get_all(db: DB):
    return await crud_genres.get_all(db)


@router.post("/create", summary="Создание нового жанра")
async def create_genre(db: DB, genre: GenreBase):
    try:
        genre_model = m_genre(**(genre.dict()))
        created_genre = await crud_genres.create(db, genre_model)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить жанр в БД")

    return created_genre
