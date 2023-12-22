import json

import pytest
from fastapi import status
from pytest_mock import MockerFixture

from src.schemas.books import BookIn
from tests.config import CREATED_BOOK, INSERT_BOOKS_DATA, INSERT_BOOKS_RESPONSE, test_user_auth_headers
from tests.conftest import add_data_to_tables
from tests.utils import generate_guid


class TestBooks:
    @pytest.mark.asyncio
    async def test_get_book(self, client, db_session, mocker: MockerFixture):
        await add_data_to_tables(db_session, INSERT_BOOKS_DATA)
        mocker.patch("src.api.v1.books.checkAuth", return_value=None)
        response = client.get(f"/books/{generate_guid(0)}", headers=test_user_auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == INSERT_BOOKS_RESPONSE

    @pytest.mark.asyncio
    async def test_create_book(self, client, db_session, mocker: MockerFixture):
        await add_data_to_tables(db_session, INSERT_BOOKS_DATA)
        book_data = json.loads(
            json.dumps(
                BookIn(title="twilight", authors=[generate_guid(0)], genres=[generate_guid(0)]).dict(), default=str
            )
        )
        mocker.patch("src.api.v1.books.checkAuth", return_value=None)
        response = client.post("/books/create", json=book_data, headers=test_user_auth_headers)
        response_data = response.json()
        response_data.pop("guid")
        assert response.status_code == status.HTTP_201_CREATED
        assert response_data == CREATED_BOOK

    @pytest.mark.asyncio
    async def test_delete_book(self, client, db_session, mocker: MockerFixture):
        await add_data_to_tables(db_session, INSERT_BOOKS_DATA)
        mocker.patch("src.api.v1.books.checkAuth", return_value=None)
        response = client.delete(f"/books/{generate_guid(0)}", headers=test_user_auth_headers)
        assert response.status_code == status.HTTP_200_OK
        response = client.get(f"/books/{generate_guid(0)}", headers=test_user_auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
