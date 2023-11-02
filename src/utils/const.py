from enum import StrEnum

GENRES_NOT_FOUND = "Не найдены жанры по данным идентификаторам"
AUTHORS_NOT_FOUND = "Не найдены авторы по данным идентификаторам"
INVALID_COORDINATES = "Некорректные значения координат"
MAX_LATITUDE = 90
MAX_LONGITUDE = 180


class GenreEnum(StrEnum):
    DETECTIVE = "detective"
    DRAMA = "drama"
    EDUCATIONAL = "educational"


class PostTypeEnum(StrEnum):
    REVIEW = "review"
    OTHER = "other"
