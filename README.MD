че-то тут будет

запустить сервер:
./start.sh

url бд в .env

http://0.0.0.0:8080/docs#/books/get_all_books_all_get

поправить стили:
black ./ && ruff --show-source --fix --exit-non-zero-on-fix ./ && flake8 --statistics ./src

создать новую миграцию на основе изменений в модели данных:
alembic revision --autogenerate -m “крутое изменение”

накатить изменения:
alembic upgrade head

откатить:
alembic downgrade -1 (или по номеру версииб см migrations/versions)

