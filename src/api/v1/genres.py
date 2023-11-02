from fastapi import APIRouter, Query, HTTPException

from src.api.dependency import DB, Credentials
from src.crud.books import DBGenre
from src.schemas.books import Genre, GenreBase
from src.model.books import Genre as m_genre

from src.utils.exceptions import checkAuth

router = APIRouter(prefix="/genres", tags=["genres"])
DEFAULT_LIST_GENRES = Query(default=None, description="List of genres")

crud_genres = DBGenre()

@router.get("/all", summary="Список всех жанров", response_model=list[Genre])
async def get_all(credentials: Credentials, db: DB):
    await checkAuth(db, credentials.credentials)
    return await crud_genres.get_all(db)


@router.post("/create", summary="Создание нового жанра")
async def create_genre(credentials: Credentials, db: DB, genre: GenreBase):
    await checkAuth(db, credentials.credentials)

    try:
        genre_model = m_genre(**(genre.dict()))
        created_genre = await crud_genres.create(db, genre_model)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось сохранить жанр в БД")

    return created_genre
