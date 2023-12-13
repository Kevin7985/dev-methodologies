from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from src.main import app as main_app
from src.database import Base, get_session

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

Session = async_sessionmaker(engine, expire_on_commit=False)

async def add_data_to_tables(conn, tables: dict):
    for table, data in tables.items():
        await conn.execute(table.__table__.insert(), data)


def replace_jsonb_with_json(tables: list):
    for table in tables:
        for column in table.__table__.columns:
            if column.type.__class__.__name__ == "JSONB":
                column.type = JSON()


@pytest_asyncio.fixture
async def alembic_config():
    return {"file": "../alembic.ini", "script_location": "../migration"}


@pytest_asyncio.fixture()
async def app():
    # replace_jsonb_with_json(replace_jsonb_with_json_tables)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # await add_data_to_tables(conn, TABLES_NEED_DATA)
    yield main_app
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(app: FastAPI, mocker: MockerFixture):
    connection = await engine.connect()
    transaction = await connection.begin()
    session = Session(bind=connection)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client(app: FastAPI, db_session: Session) -> AsyncGenerator:
    async def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    async def async_dummy():
        pass

    app.dependency_overrides[get_session] = _get_test_db
    app.router.startup = async_dummy
    with TestClient(app) as client:
        yield client