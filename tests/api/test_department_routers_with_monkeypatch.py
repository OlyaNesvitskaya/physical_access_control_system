import pytest
from httpx import AsyncClient
from services.department_service import DepartmentService
from routers import department_router


url_prefix = department_router.prefix
pytestmark = pytest.mark.anyio


async def test_mock_department_create(authorized_superuser: AsyncClient, monkeypatch):
    data = {'id': 1, 'name': 'dep_1'}

    async def mock_create(*args, **kwargs):
        return data

    monkeypatch.setattr(DepartmentService, "create", mock_create)
    response = await authorized_superuser.post(f"{url_prefix}", json=data)
    assert response.status_code == 200
    assert response.json() == data


async def test_mock_department_get(authorized_superuser: AsyncClient, monkeypatch):
    test_data = {"id": 1, "name": "dep_1"}

    async def mock_get(*args, **kwargs):
        return test_data

    monkeypatch.setattr(DepartmentService, "get", mock_get)

    response = await authorized_superuser.get(f"{url_prefix}/1")
    assert response.status_code == 200
    assert response.json() == test_data


async def test_mock_department_update(authorized_superuser: AsyncClient, monkeypatch):
    test_data = {"id": 1, "name": "dep_7"}

    async def mock_patch(*args, **kwargs):
        return test_data

    monkeypatch.setattr(DepartmentService, "update", mock_patch)

    response = await authorized_superuser.patch(f"{url_prefix}/1", json=test_data)
    assert response.status_code == 200
    assert response.json() == test_data


async def test_mock_department_delete(authorized_superuser: AsyncClient, monkeypatch):

    async def mock_delete(*args, **kwargs):
        return None

    monkeypatch.setattr(DepartmentService, "delete", mock_delete)

    response = await authorized_superuser.delete(f"{url_prefix}/1")
    assert response.status_code == 204


