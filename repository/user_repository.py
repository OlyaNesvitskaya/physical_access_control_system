from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db_connection
from models import User
from repository.repository_meta import RepositoryMeta


class UserRepository(RepositoryMeta):
    session: AsyncSession

    def __init__(
            self, session: AsyncSession = Depends(get_db_connection)
    ) -> None:
        self.session = session

    async def create(self, user: User) -> User:
        """Write user to database."""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        """Read user from database."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update(
        self, user: User
    ) -> User:
        self.session.add(user)
        await self.session.commit()
        return user

    async def delete(
        self, user: User
    ) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def get(
            self, user_id: int
    ) -> User | None:
        return await self.session.get(User, user_id)

    async def list(
        self, limit: Optional[int], start: Optional[int],
    ) -> Sequence[User]:
        result = await self.session.execute(select(User).limit(limit).offset(start))
        return result.scalars().all()
