import pytest
from httpx import AsyncClient
from datetime import datetime
from models import Employee
from routers import employee_router

url_prefix = employee_router.prefix
pytestmark = pytest.mark.anyio


async def test_get_employee(authorized_superuser: AsyncClient, employee: Employee) -> None:

    response = await authorized_superuser.get(f"{url_prefix}/1")

    assert response.status_code == 200
    assert response.json() == {'name': 'Anna', 'surname': 'Karenina',
                               'department_id': 1, 'card_id': 11111111,
                               'card_start_date': datetime.today().strftime('%Y-%m-%d'),
                               'card_finish_date': datetime.today().strftime('%Y-%m-%d'),
                               'id': 1
                               }


async def test_get_all_employees(authorized_superuser: AsyncClient, employee) -> None:
    response = await authorized_superuser.get(f"{url_prefix}")

    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'Anna', 'surname': 'Karenina',
                               'department_id': 1, 'card_id': 11111111,
                               'card_start_date': datetime.today().strftime('%Y-%m-%d'),
                               'card_finish_date': datetime.today().strftime('%Y-%m-%d')
                               }]
    assert len(response.json()) == 1


async def test_update_employee(authorized_superuser: AsyncClient, employee: Employee) -> None:

    data = {'card_id': 12121212}
    response = await authorized_superuser.patch(f"{url_prefix}/1", json=data)

    assert response.status_code == 200
    assert response.json().get('card_id') == data['card_id']


async def test_delete_employee(authorized_superuser: AsyncClient, employee: Employee) -> None:

    response = await authorized_superuser.delete(f"{url_prefix}/1")

    assert response.status_code == 204


async def test_create_employee(authorized_superuser: AsyncClient, department) -> None:
    data = {
        'id': 1,
        'name': 'Anna',
        'surname': 'Karenina',
        'department_id': department.id,
        'card_id': 11111111,
        'card_start_date': datetime.today().strftime('%Y-%m-%d'),
        'card_finish_date': datetime.today().strftime('%Y-%m-%d')}

    response = await authorized_superuser.post(f"{url_prefix}", json=data)
    assert response.status_code == 200
    assert response.json() == data








