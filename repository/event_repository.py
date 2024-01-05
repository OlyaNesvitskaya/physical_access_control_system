from repository.repository_meta import RepositoryMeta
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db_connection
from models import Event


class EventRepository(RepositoryMeta):
    session: AsyncSession

    def __init__(
        self, session: AsyncSession = Depends(get_db_connection)
    ) -> None:
        self.session = session

    async def create(
        self, event: Event
    ) -> None:
        self.session.add(event)
        await self.session.commit()


