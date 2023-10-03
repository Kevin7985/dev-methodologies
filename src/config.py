import structlog
from fastapi_offline import FastAPIOffline
from starlette.middleware.cors import CORSMiddleware

from src.settings import Settings

# FastAPICache.init(InMemoryBackend(), key_builder=custom_key_builder)  # noqa: E800


settings = Settings(_env_file=".env")


app = FastAPIOffline(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
)

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=True),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    cache_logger_on_first_use=True,
)
log = structlog.get_logger()


# def get_auth_service():  # noqa: E800
#     auth_service = FastAPIKeycloak(  # noqa: E800
#         server_url=settings.keycloak_url,  # noqa: E800
#         client_id=settings.client_id,  # noqa: E800
#         client_secret=settings.client_secret,  # noqa: E800
#         admin_client_secret=settings.admin_client_secret,  # noqa: E800
#         realm=settings.realm,  # noqa: E800
#         callback_uri=settings.callback_uri,  # noqa: E800
#     )  # noqa: E800
#     auth_service.add_swagger_config(app)  # noqa: E800
#     yield auth_service  # noqa: E800
