from src.model.books import Author, Book, Book_Author, Book_Genre, Genre

test_user_token = "token"
test_user_auth_headers = {"Authorization": f"Bearer {test_user_token}"}

test_user = {
    "guid": "00000000-0000-0000-0000-000000000000",
    "login": "warmbookworm",
    "name": "федя",
    "avatar": "пикча",
    "email": "почта@test.ru",
    "password": "creativepassword",
    "phone": "+78005553535",
}

test_book = {
    "guid": "00000000-0000-0000-0000-000000000000",
    "title": "Название книги",
    "description": "Описание книги",
    "rating": 5,
    "isbn": "IBSN книги",
    "pic_file_name": "Обложка книги",
}

test_author = {
    "guid": "00000000-0000-0000-0000-000000000000",
    "name": "Наталья",
    "surname": "Башилова",
    "patronymic": "Ивановна",
}

test_genre = {"guid": "00000000-0000-0000-0000-000000000000", "name": "Ужасы"}

test_book_genre = {
    "book_id": "00000000-0000-0000-0000-000000000000",
    "genre_id": "00000000-0000-0000-0000-000000000000",
}

test_book_author = {
    "book_id": "00000000-0000-0000-0000-000000000000",
    "author_id": "00000000-0000-0000-0000-000000000000",
}


INSERT_BOOKS_DATA = {
    Book: [test_book],
    Author: [test_author],
    Genre: [test_genre],
    Book_Genre: [test_book_genre],
    Book_Author: [test_book_author],
}

INSERT_BOOKS_RESPONSE = {
    "authors": [
        {
            "guid": "00000000-0000-0000-0000-000000000000",
            "name": "Наталья",
            "patronymic": "Ивановна",
            "surname": "Башилова",
        }
    ],
    "description": "Описание книги",
    "genres": [{"guid": "00000000-0000-0000-0000-000000000000", "name": "Ужасы"}],
    "guid": "00000000-0000-0000-0000-000000000000",
    "isbn": "IBSN книги",
    "pic_file_name": "Обложка книги",
    "rating": 5.0,
    "title": "Название книги",
}

CREATED_BOOK = {
    "authors": [
        {
            "guid": "00000000-0000-0000-0000-000000000000",
            "name": "Наталья",
            "patronymic": "Ивановна",
            "surname": "Башилова",
        }
    ],
    "description": None,
    "genres": [{"guid": "00000000-0000-0000-0000-000000000000", "name": "Ужасы"}],
    "isbn": None,
    "pic_file_name": None,
    "rating": None,
    "title": "twilight",
}
