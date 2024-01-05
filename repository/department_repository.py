from typing import Optional, Sequence
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from repository.repository_meta import RepositoryMeta
from core.database import get_db_connection
from models import Department


class DepartmentRepository(RepositoryMeta):
    session: AsyncSession

    def __init__(
        self, session: AsyncSession = Depends(get_db_connection)
    ) -> None:
        self.session = session

    async def list(
        self, limit: Optional[int], start: Optional[int],
    ) -> Sequence[Department]:
        result = await self.session.execute(select(Department).limit(limit).offset(start))
        return result.scalars().all()

    async def get(
        self, department_id: int
    ) -> Department | None:
        return await self.session.get(Department, department_id)

    async def create(
        self, department: Department
    ) -> Department:
        self.session.add(department)
        await self.session.commit()
        await self.session.refresh(department)
        return department

    async def update(
        self, department: Department
    ) -> Department:
        await self.session.merge(department)
        await self.session.commit()
        return department

    async def delete(
        self, department: Department
    ) -> None:
        await self.session.delete(department)
        await self.session.commit()

