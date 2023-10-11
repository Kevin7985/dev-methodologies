from enum import StrEnum


class GenreEnum(StrEnum):
    DETECTIVE = "detective"
    DRAMA = "drama"
    EDUCATIONAL = "educational"


class PostTypeEnum(StrEnum):
    REVIEW = "review"
    OTHER = "other"
