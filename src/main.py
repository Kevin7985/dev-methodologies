import stackprinter
import uvicorn
from fastapi_pagination import add_pagination

from src.api.v1 import authors, book_requests, bookcrossing_points, books, comments, genres, likes, posts, users
from src.config import app

# TODO: automatically include all available routers
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(bookcrossing_points.router)
app.include_router(book_requests.router)
app.include_router(genres.router)
app.include_router(posts.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(users.router)

add_pagination(app)


if __name__ == "__main__":
    stackprinter.set_excepthook()
    uvicorn.run(app, host="127.0.0.1", port=8080)
