import stackprinter
import uvicorn
from fastapi_pagination import add_pagination

from src.api.v1 import books, users
from src.config import app

# TODO: automatically include all available routers
app.include_router(users.router)
app.include_router(books.router)

add_pagination(app)


if __name__ == "__main__":
    stackprinter.set_excepthook()
    uvicorn.run(app, host="127.0.0.1", port=8080)