import os
from collections.abc import AsyncGenerator

import redis
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

load_dotenv()

db_url = os.environ.get("POSTGRES_DB_URL")
redis_url = os.environ.get("REDIS_DB_URL")
redis_password = os.environ.get("REDIS_PASSWORD")

engine = create_async_engine(db_url, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

Redis = redis.from_url(url=redis_url, password=redis_password)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
