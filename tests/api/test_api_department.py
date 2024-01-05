import pytest
from httpx import AsyncClient
from models import Department
from routers import department_router


url_prefix = department_router.prefix

pytestmark = pytest.mark.anyio


async def test_get_department(authorized_superuser: AsyncClient, department: Department) -> None:

    response = await authorized_superuser.get(f"{url_prefix}/1")

    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'dep1'}


async def test_get_all_department(authorized_superuser: AsyncClient, department: Department) -> None:
    response = await authorized_superuser.get(f"{url_prefix}")

    assert response.status_code == 200
    assert response.json() == [department.to_dict()]
    assert len(response.json()) == 1


async def test_update_department(authorized_superuser: AsyncClient, department: Department) -> None:

    data = {'name': 'HR'}
    response = await authorized_superuser.patch(f"{url_prefix}/1", json=data)

    assert response.status_code == 200
    assert response.json().get('name') == data['name']


async def test_delete_department(authorized_superuser: AsyncClient, department: Department) -> None:

    response = await authorized_superuser.delete(f"{url_prefix}/1")

    assert response.status_code == 204


async def test_create_department(authorized_superuser: AsyncClient) -> None:

    data = {'id': 1, 'name': 'dep_1'}

    response = await authorized_superuser.post(f"{url_prefix}", json=data)

    assert response.status_code == 200
    assert response.json() == data




