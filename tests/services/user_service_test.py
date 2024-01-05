import pytest
from fastapi import HTTPException
from services import UserService
from schemas.user_schema import UserSchema, UpdateUserSchema

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    'page_size, start_index, number_of_records',
    [
        (1, 0, 1),
        (0, 0, 0)
    ]
)
async def test_list(page_size, start_index, number_of_records, fake_user_repository):

    retrieved = await UserService(fake_user_repository).list(page_size=page_size, start_index=start_index)

    assert len(retrieved) == number_of_records


async def test_get(fake_user_repository):

    first_user = fake_user_repository.items[0]
    retrieved = await UserService(fake_user_repository).get(first_user.id)

    assert retrieved.id == first_user.id
    assert retrieved.email == first_user.email


async def test_error_get(fake_user_repository):

    with pytest.raises(HTTPException) as excinfo:
        await UserService(fake_user_repository).get(100)

    assert excinfo.type is HTTPException


async def test_update(fake_user_repository):

    first_user = fake_user_repository.items[0]
    retrieved = await (UserService(fake_user_repository)
                       .update(first_user.id, UpdateUserSchema(email='update_user1@gmail.com')))

    assert retrieved.id == first_user.id
    assert retrieved.email == 'update_user1@gmail.com'


@pytest.mark.parametrize(
    'user_id, user_body, type_exception, exception_value',
    [
        (1, UpdateUserSchema(email='user2@gmail.com'), HTTPException,
         "(409, 'User with email:user2@gmail.com already exist.')"),

        (100, UpdateUserSchema(email='user2@gmail.com'), HTTPException,
         "(400, 'User with supplied ID does not exist.')"),
    ]
)
async def test_error_update(user_id, user_body, fake_user_repository,
                            type_exception, exception_value):

    with pytest.raises(type_exception) as excinfo:
        await UserService(fake_user_repository).update(user_id, user_body)

    assert excinfo.type is type_exception
    assert str(excinfo.value) == exception_value


async def test_create(fake_user_repository):

    new_user = UserSchema(email='new_user@gmail.com', password='new_user')
    retrieved = await UserService(fake_user_repository).create(new_user)

    assert retrieved.email == new_user.email
    assert retrieved.is_superuser == new_user.is_superuser


async def test_error_create(fake_user_repository):

    with pytest.raises(HTTPException) as excinfo:
        await UserService(fake_user_repository).create(UserSchema(email='new_user@gmail.com', password='new_user'))

    assert excinfo.type is HTTPException


async def test_delete(fake_user_repository):

    retrieved = await (UserService(fake_user_repository)
                       .delete(fake_user_repository.items[-1].id))

    assert retrieved is None


async def test_error_delete(fake_user_repository):

    with pytest.raises(HTTPException) as excinfo:
        await UserService(fake_user_repository).delete(100)

    assert excinfo.type is HTTPException


