from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user_schema import TokenSchema
from services.user_service import UserService
from core.environment import settings


auth_router = APIRouter(prefix=f"/{settings.AUTH_URL}", tags=["Authentication"], include_in_schema=False)


@auth_router.post("", response_model=TokenSchema)
async def authenticate(
    login: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends()
) -> TokenSchema | None:

    """User authentication.
    Returns:
        Access token.
    """
    return await user_service.authenticate(login)
