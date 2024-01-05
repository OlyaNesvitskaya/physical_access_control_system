from datetime import datetime
import pytest
from httpx import AsyncClient
from services.employee_service import EmployeeService
from routers import employee_router

url_prefix = employee_router.prefix
pytestmark = pytest.mark.anyio


def get_employee_data():
    return {
        'id': 1,
        'name': 'Anna',
        'surname': 'Karenina',
        'department_id': 1,
        'card_id': 11111111,
        'card_start_date': datetime.today().strftime('%Y-%m-%d'),
        'card_finish_date': datetime.today().strftime('%Y-%m-%d')
}


async def test_mock_employee_create(authorized_superuser: AsyncClient, monkeypatch):
    data = get_employee_data()

    async def mock_create(*args, **kwargs):
        return data

    monkeypatch.setattr(EmployeeService, "create", mock_create)
    response = await authorized_superuser.post(f"{url_prefix}", json=data)
    assert response.status_code == 200
    assert response.json() == data


async def test_mock_employee_get(authorized_superuser: AsyncClient, monkeypatch):
    data = get_employee_data()

    async def mock_get(*args, **kwargs):
        return data

    monkeypatch.setattr(EmployeeService, "get", mock_get)

    response = await authorized_superuser.get(f"{url_prefix}/1")
    assert response.status_code == 200
    assert response.json() == data


async def test_mock_employee_update(authorized_superuser: AsyncClient, monkeypatch):
    data = {
        'card_id': 4545454
    }

    async def mock_patch(*args, **kwargs):
        get_employee_data().update(data)
        return get_employee_data()

    monkeypatch.setattr(EmployeeService, "update", mock_patch)

    response = await authorized_superuser.patch(f"{url_prefix}/1", json=data)
    assert response.status_code == 200
    assert response.json() == get_employee_data()


async def test_mock_employee_delete(authorized_superuser, monkeypatch):

    async def mock_delete(*args, **kwargs):
        return None

    monkeypatch.setattr(EmployeeService, "delete", mock_delete)

    response = await authorized_superuser.delete(f"{url_prefix}/1")
    assert response.status_code == 204


