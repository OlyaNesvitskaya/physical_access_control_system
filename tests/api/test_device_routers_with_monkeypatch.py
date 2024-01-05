import pytest
from httpx import AsyncClient
from services.device_service import DeviceService
from routers import device_router

url_prefix = device_router.prefix
pytestmark = pytest.mark.anyio


def get_device_data():
    return {
        'id': 1,
        'name': 'Contact reader №1', 'imei': '111111qwerty',
        'route': 'enter', 'department_id': 1, 'opened': False 
    }


async def test_mock_device_create(authorized_superuser: AsyncClient, monkeypatch):
    data = get_device_data()

    async def mock_create(*args, **kwargs):
        return data

    monkeypatch.setattr(DeviceService, "create", mock_create)
    response = await authorized_superuser.post(f"{url_prefix}", json=data)
    assert response.status_code == 200
    assert response.json() == data


async def test_mock_device_get(authorized_superuser: AsyncClient, monkeypatch):
    data = get_device_data()

    async def mock_get(*args, **kwargs):
        return data

    monkeypatch.setattr(DeviceService, "get", mock_get)

    response = await authorized_superuser.get(f"{url_prefix}/1")
    assert response.status_code == 200
    assert response.json() == data


async def test_mock_device_update(authorized_superuser: AsyncClient, monkeypatch):
    data = {
        'imei': '4678090'
    }

    async def mock_patch(*args, **kwargs):
        get_device_data().update(data)
        return get_device_data()
    monkeypatch.setattr(DeviceService, "update", mock_patch)

    response = await authorized_superuser.patch(f"{url_prefix}/1", json=data)
    assert response.status_code == 200
    assert response.json() == get_device_data()


async def test_mock_device_delete(authorized_superuser: AsyncClient, monkeypatch):

    async def mock_delete(*args, **kwargs):
        return None

    monkeypatch.setattr(DeviceService, "delete", mock_delete)

    response = await authorized_superuser.delete(f"{url_prefix}/1")
    assert response.status_code == 204


