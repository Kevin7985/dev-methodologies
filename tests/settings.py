from pydantic import Field

from src.settings import Settings


class BaseTestSettings(Settings):
    db_host: str = Field("localhost", env="DB_HOST")
    db_port: str = Field("5432", env="DB_PORT")
    db_name: str = Field("test_db", env="DB_DATABASE")
    db_user: str = Field("admin", env="DB_USER")
    db_password: str = Field("admin", env="DB_PASSWORD")
    database_url: str = Field("sqlite:///./test.db", env="DB_URL")

    class Config:
        env_file = "../.env"
