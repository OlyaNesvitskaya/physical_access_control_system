import pytest
from httpx import AsyncClient
from models import User
from routers import user_router


url_prefix = user_router.prefix

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize('client, status_code', [
    (pytest.lazy_fixture('authorized_not_superuser'), 403),
    (pytest.lazy_fixture('authorized_superuser'), 200),
])
async def test_get_user(client: AsyncClient, not_superuser: User, status_code:int) -> None:

    response = await client.get(f"{url_prefix}/{not_superuser.id}")
    assert response.status_code == status_code

    if client == 'authorized_superuser':
        assert response.json() == {'id': not_superuser.id, 'email': not_superuser.email}


@pytest.mark.parametrize('client, status_code', [
    (pytest.lazy_fixture('authorized_not_superuser'), 403),
    (pytest.lazy_fixture('authorized_superuser'), 200),
])
async def test_get_all_user(client: AsyncClient, status_code: int, not_superuser: User) -> None:
    response = await client.get(f"{url_prefix}")

    assert response.status_code == status_code

    if client == 'authorized_superuser':
        assert len(response.json()) == 2


@pytest.mark.parametrize('client, status_code', [
    (pytest.lazy_fixture('authorized_not_superuser'), 403),
    (pytest.lazy_fixture('authorized_superuser'), 200),
])
async def test_update_user(client: AsyncClient,  status_code: int, user3) -> None:

    data = {'email': "new_email@gmail.com"}
    response = await client.patch(f"{url_prefix}/{user3.id}", json=data)

    assert response.status_code == status_code

    if client == 'authorized_superuser':
        assert response.json().get('email') == data['email']


@pytest.mark.parametrize('client, status_code', [
    (pytest.lazy_fixture('authorized_not_superuser'), 403),
    (pytest.lazy_fixture('authorized_superuser'), 200),
])
async def test_create_user(client: AsyncClient, status_code: int) -> None:

    data = {'email': 'user3@gmail.com', 'password': '3333', 'is_superuser': False}

    response = await client.post(f"{url_prefix}", json=data)

    assert response.status_code == status_code

    if client == 'authorized_superuser':
        assert response.json().get('email') == data['email']


@pytest.mark.parametrize('client, status_code', [
    (pytest.lazy_fixture('authorized_not_superuser'), 403),
    (pytest.lazy_fixture('authorized_superuser'), 204),
])
async def test_delete_user(client: AsyncClient, not_superuser: User, status_code: int) -> None:

    response = await client.delete(f"{url_prefix}/2")

    assert response.status_code == status_code
















