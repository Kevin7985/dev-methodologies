from enum import StrEnum

GENRES_NOT_FOUND = "Не найдены жанры по данным идентификаторам"
AUTHORS_NOT_FOUND = "Не найдены авторы по данным идентификаторам"


class GenreEnum(StrEnum):
    DETECTIVE = "detective"
    DRAMA = "drama"
    EDUCATIONAL = "educational"


class PostTypeEnum(StrEnum):
    REVIEW = "review"
    OTHER = "other"
