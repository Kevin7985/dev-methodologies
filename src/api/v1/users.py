from fastapi import APIRouter

from src.api.dependency import DB, Credentials

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})


@router.get("/all", summary="Список всех пользователей")
async def get_all(db: DB, credentials: Credentials):
    return "hello"
