import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Event, Device, Employee
from repository import EventRepository


@pytest.mark.anyio
async def test_device_repository_can_create(session: AsyncSession, device: Device, employee: Employee):
    new_event = Event(device_id=device.id, employee_id=employee.id, success=True)

    repo = EventRepository(session)
    await repo.create(new_event)

    res = await session.execute(select(Event).limit(1))
    retrieved_event = res.scalar_one_or_none()

    assert retrieved_event.device_id == new_event.device_id
    assert retrieved_event.employee_id == new_event.employee_id
    assert retrieved_event.success == new_event.success



