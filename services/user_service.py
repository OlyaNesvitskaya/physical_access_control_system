from datetime import timedelta, datetime
from typing import Optional, Sequence

from fastapi import Depends, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import exc

from core.environment import settings
from exc import raise_with_log
from models import User
from repository import UserRepository
from schemas.user_schema import TokenSchema, UserSchema, UpdateUserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashingMixin:
    """Hashing and verifying passwords."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""

        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate a bcrypt hashed password."""

        return pwd_context.hash(password)


class UserService(HashingMixin):

    def __init__(
        self, user_repository: UserRepository = Depends()
    ) -> None:
        self.user_repository = user_repository

    async def create(self, user_body: UserSchema) -> User:
        """Add user with hashed password to database."""

        try:
            return await self.user_repository.create(
                User(
                    email=user_body.email,
                    hashed_password=self.get_password_hash(user_body.password),
                    is_superuser=user_body.is_superuser,
                )
            )
        except exc.IntegrityError as e:
            raise_with_log(status_code=409,
                           detail=f"User with email:{user_body.email} already exist.")

    async def get_by_email(self, email: str) -> User | None:
        user = await self.user_repository.get_by_email(email)
        return user

    async def get(self, user_id: int) -> User | None:
        user = await self.user_repository.get(user_id)

        if not user:
            raise_with_log(status_code=400,
                           detail="User with supplied ID does not exist.")

        return user

    async def authenticate(
        self, login
    ) -> TokenSchema | None:
        """Generate token.

        Obtains username and password and verifies password against
        hashed password stored in database. If valid then temporary
        token is generated, otherwise the corresponding exception is raised.
        """

        user = await self.get_by_email(email=login.username)

        if not user:
            raise_with_log(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

        if not self.verify_password(login.password, user.hashed_password):
            raise_with_log(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        access_token = self._create_access_token(email=login.username)

        return TokenSchema(access_token=access_token, token_type=settings.TOKEN_TYPE)

    def _create_access_token(self,  email: str) -> str:
        """Encode user information and expiration time."""

        payload = {
            "sub": email,
            "expires_at": self._expiration_time(),
        }
        print(jwt.encode({
            "expires_at": self._expiration_time(),
        }, settings.TOKEN_KEY,
                          algorithm=settings.TOKEN_ALGORITHM))
        return jwt.encode(payload, settings.TOKEN_KEY,
                          algorithm=settings.TOKEN_ALGORITHM)

    @staticmethod
    def _expiration_time() -> str:
        """Get token expiration time."""

        expires_at = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")

    async def delete(
        self, user_id: int
    ) -> None:

        user = await self.get(user_id)
        await self.user_repository.delete(user)

    async def list(
        self, page_size: Optional[int] = 100, start_index: Optional[int] = 0,
    ) -> Sequence[User]:
        return await self.user_repository.list(page_size, start_index)

    async def update(
        self, user_id: int, user_body: UpdateUserSchema
    ) -> User:
        user = await self.get(user_id)
        user_body = user_body.model_dump(exclude_unset=True)
        for key, value in user_body.items():
            setattr(user, key, value)
        try:
            return await self.user_repository.update(user)
        except exc.IntegrityError as e:
            raise_with_log(status_code=409,
                           detail=f"User with email:{user_body.get('email', '')} already exist.")

