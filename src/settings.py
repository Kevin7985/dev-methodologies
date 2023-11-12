from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field(env="POSTGRES_DB_URL")
    back_token: str = Field(env="BACK_TOKEN")
    
    class Config:
        env_file = "../.env"
