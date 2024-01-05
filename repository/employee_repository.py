from typing import Optional, Sequence
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from core.database import get_db_connection
from repository.repository_meta import RepositoryMeta
from models import Employee


class EmployeeRepository(RepositoryMeta):
    session: AsyncSession

    def __init__(
        self, session: AsyncSession = Depends(get_db_connection)
    ) -> None:
        self.session = session

    async def list(
        self, limit: Optional[int], start: Optional[int],
    ) -> Sequence[Employee]:
        result = await self.session.execute(select(Employee).limit(limit).offset(start))
        return result.scalars().all()

    async def get(
            self, employee_id: int, bound_devices=False
    ) -> Employee | None:
        result = await self.session.get(Employee, employee_id)
        if bound_devices:
            await result.awaitable_attrs.devices
        return result

    async def create(
        self, employee: Employee
    ) -> Employee:
        self.session.add(employee)
        await self.session.commit()
        await self.session.refresh(employee)
        return employee

    async def update(
        self, employee: Employee
    ) -> Employee:
        self.session.add(employee)
        await self.session.commit()
        return employee

    async def delete(
        self, employee: Employee
    ) -> None:
        await self.session.delete(employee)
        await self.session.commit()

    async def get_by_card_id(self, card_id: int) -> Employee:
        result = await self.session.execute(
            select(Employee).where(Employee.card_id == card_id).options(selectinload(Employee.devices)))
        return result.scalar_one_or_none()

