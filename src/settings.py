from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field(env="POSTGRES_DB_URL")
    
    class Config:
        env_file = "../.env"
