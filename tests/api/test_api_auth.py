import pytest
from httpx import AsyncClient
from routers import auth_router

url_prefix = auth_router.prefix

pytestmark = pytest.mark.anyio


async def test_authenticate(async_client: AsyncClient, superuser) -> None:

    data = {'username': 'superuser@gmail.com', 'password': 'superuser'}

    response = await async_client.post(f"{url_prefix}", data=data)

    assert response.status_code == 200


@pytest.mark.parametrize(
    'data, response_detail',
    [
     ({'username': 'some_user@gmail.com', 'password': 'some_password'}, 'Incorrect username or password'),
     ({'username': 'superuser@gmail.com', 'password': 'some_password'}, 'Incorrect password')
    ]
)
async def test_authenticate_error(async_client: AsyncClient, data, response_detail) -> None:

    response = await async_client.post(f"{url_prefix}", data=data)

    assert response.status_code == 401
    assert response.json()['detail'] == response_detail





