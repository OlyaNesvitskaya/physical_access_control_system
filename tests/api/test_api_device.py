from httpx import AsyncClient
import pytest
from models import Device
from routers import device_router

url_prefix = device_router.prefix
pytestmark = pytest.mark.anyio


async def test_get_device(authorized_superuser: AsyncClient, device: Device) -> None:

    response = await authorized_superuser.get(f"{url_prefix}/1")

    assert response.status_code == 200
    assert response.json() == device.to_dict()


async def test_get_all_devices(authorized_superuser: AsyncClient, device) -> None:

    response = await authorized_superuser.get(f"{url_prefix}")

    assert response.status_code == 200
    assert response.json() == [device.to_dict()]
    assert len(response.json()) == 1


async def test_update_device(authorized_superuser: AsyncClient, device: Device) -> None:

    data = {'imei': "555qwerty"}
    response = await authorized_superuser.patch(f"{url_prefix}/1", json=data)

    assert response.status_code == 200
    assert response.json().get('imei') == data['imei']


async def test_delete_device(authorized_superuser: AsyncClient, device: Device) -> None:

    response = await authorized_superuser.delete(f"{url_prefix}/1")

    assert response.status_code == 204


async def test_create_device(authorized_superuser: AsyncClient, department) -> None:
    data = {
        'id': 1,
        'name': 'Contact reader №1', 'imei': '111111qwerty',
        'route': 'enter', 'department_id': 1, 'opened': False
    }

    response = await authorized_superuser.post(f"{url_prefix}", json=data)

    assert response.status_code == 200
    assert response.json() == data








