import stackprinter
import uvicorn
from fastapi_pagination import add_pagination

from src.api.v1 import authors, bookcrossing_points, books, genres, users, posts, likes, comments
from src.config import app

# TODO: automatically include all available routers
app.include_router(authors.router)
app.include_router(bookcrossing_points.router)
app.include_router(books.router)
app.include_router(genres.router)
app.include_router(posts.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(users.router)

add_pagination(app)


if __name__ == "__main__":
    stackprinter.set_excepthook()
    uvicorn.run(app, host="127.0.0.1", port=8080)
