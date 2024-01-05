from typing import Optional, Sequence, Tuple
from fastapi import Depends
from sqlalchemy import select, Row
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from repository.repository_meta import RepositoryMeta
from core.database import get_db_connection
from models import Device


class DeviceRepository(RepositoryMeta):
    session: AsyncSession

    def __init__(
        self, session: AsyncSession = Depends(get_db_connection)
    ) -> None:
        self.session = session

    async def list(
        self, limit: Optional[int], start: Optional[int],
    ) -> Sequence[Device]:
        result = await self.session.execute(select(Device).limit(limit).offset(start))
        return result.scalars().all()

    async def get(self, device_id: int, bound_employees=False) -> Device | None:
        result = await self.session.get(Device, device_id)
        if bound_employees:
            await result.awaitable_attrs.employees
        return result

    async def create(self, device: Device) -> Device:
        self.session.add(device)
        await self.session.commit()
        await self.session.refresh(device)
        return device

    async def update(self, device: Device) -> Device:
        self.session.add(device)
        await self.session.commit()
        return device

    async def delete(self, device: Device) -> None:
        await self.session.delete(device)
        await self.session.commit()

    async def get_device_id_and_device_opened(self, imei: str) -> Row[Tuple[int, str]] | None:
        stmt = select(Device).options(load_only(Device.opened)
                                      ).where(Device.imei == imei)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


