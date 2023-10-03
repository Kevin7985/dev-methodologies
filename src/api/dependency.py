from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

# from src.config import get_auth_service  # noqa: E800
from src.database import get_session

security = HTTPBearer()

DB = Annotated[AsyncSession, Depends(get_session)]
# IDP = Annotated[FastAPIKeycloak, Depends(get_auth_service)]  # noqa: E800
Credentials = Annotated[HTTPAuthorizationCredentials, Security(security)]
