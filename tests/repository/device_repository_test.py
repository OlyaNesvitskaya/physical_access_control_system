import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Device, Department
from repository import DeviceRepository

pytestmark = pytest.mark.anyio


async def test_device_repository_can_get(session: AsyncSession, device: Device):

    repo = DeviceRepository(session)
    retrieved_device = await repo.get(device.id)

    assert retrieved_device
    assert retrieved_device.name == device.name
    assert retrieved_device.imei == device.imei
    assert retrieved_device.route == device.route
    assert retrieved_device.department_id == device.department_id


async def test_device_repository_can_update(session: AsyncSession, device: Device):

    repo = DeviceRepository(session)

    setattr(device, 'name', 'Contact reader №2')
    setattr(device, 'imei', "222222qwerty")

    retrieved_device = await repo.update(device)

    assert retrieved_device.name == device.name
    assert retrieved_device.imei == device.imei
    assert retrieved_device.route == device.route
    assert retrieved_device.department_id == device.department_id


async def test_device_repository_can_delete(session: AsyncSession, device: Device):

    repo = DeviceRepository(session)
    retrieved_device = await repo.delete(device)

    res = await session.execute(select(Device).filter(Device.name == device.name))
    device = res.scalar_one_or_none()

    assert retrieved_device is None
    assert device is None


async def test_get_devices_list(session: AsyncSession, department: Department):
    devices_list = [
        Device(name='Contact reader №2', imei='222222qwerty', route='enter', department_id=department.id),
        Device(name='Contact reader №3', imei='333333qwerty', route='enter', department_id=department.id),
    ]

    session.add_all(devices_list)
    await session.commit()

    repo = DeviceRepository(session)
    retrieved_devices = await repo.list(limit=2, start=0)

    assert len(retrieved_devices) == 2
    for ind, obj_name in enumerate(retrieved_devices):
        assert obj_name.name == devices_list[ind].name


async def test_device_repository_can_create(session: AsyncSession, department: Department):

    new_device = Device(name='Contact reader №1', imei='111111qwerty', route='enter', department_id=department.id)

    repo = DeviceRepository(session)
    retrieved_device = await repo.create(new_device)

    assert retrieved_device.name == new_device.name
    assert retrieved_device.imei == new_device.imei
    assert retrieved_device.route == new_device.route
    assert retrieved_device.department_id == new_device.department_id


async def test_get_device_id_and_device_opened(session: AsyncSession, device: Device):

    repo = DeviceRepository(session)

    retrieved_device = await repo.get_device_id_and_device_opened(device.imei)

    assert retrieved_device.id == device.id
    assert retrieved_device.opened == device.opened


