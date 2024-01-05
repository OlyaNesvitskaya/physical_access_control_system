import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from models import *


@pytest.mark.anyio
@pytest.mark.parametrize(
    'access_to_device, has_permission',
    [
        (True, {'entry': 'Admission are permitted'}),
        (False, {'entry': 'Admission are prohibited'})

    ]
)
async def test_attempt_to_drop_in_the_door(
        authorized_superuser: AsyncClient,
        employee: Employee,
        device: Device,
        session: AsyncSession,
        access_to_device: bool,
        has_permission: dict) -> None:

    if access_to_device:
        device.employees = [employee]
        session.add(device)
        await session.commit()
    else:
        device.employees = []
        session.add(device)
        await session.commit()

    response = await authorized_superuser.get(f"/drop_in/{employee.card_id}/{device.imei}")

    assert response.status_code == 200
    assert response.json() == has_permission









