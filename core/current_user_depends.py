from datetime import datetime
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from services import UserService
from core.environment import settings
from exc import raise_with_log
from models import User


oauth2_schema = OAuth2PasswordBearer(tokenUrl=settings.AUTH_URL)


async def get_current_user(
    user_service: UserService = Depends(),
    token: str = Depends(oauth2_schema)
) -> User | None:
    """Decode token to obtain user information.
    Extracts user information from token and verifies expiration time.
    If token is valid then instance of User class is returned, otherwise exception is raised.
    """

    if token is None:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    try:
        payload = jwt.decode(token, settings.TOKEN_KEY, algorithms=[settings.TOKEN_ALGORITHM])

        sub: str = payload.get("sub")
        expires_at: str = payload.get("expires_at")

        if sub is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

        if is_expired(expires_at):
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Token expired")

        return await user_service.get_by_email(email=sub)

    except JWTError:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")


def is_expired(expires_at: str) -> bool:
    """Return :obj:`True` if token has expired."""

    return datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") < datetime.utcnow()
