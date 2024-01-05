import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User
from repository import UserRepository
from services.user_service import HashingMixin

pytestmark = pytest.mark.anyio


async def test_user_repository_get_by_id(session: AsyncSession, not_superuser: User):

    retrieved_user = await UserRepository(session).get(not_superuser.id)

    assert retrieved_user.email == not_superuser.email
    assert retrieved_user.is_superuser == not_superuser.is_superuser


async def test_user_repository_get_by_email(session: AsyncSession, not_superuser: User):

    retrieved_user = await UserRepository(session).get_by_email(email=not_superuser.email)

    assert retrieved_user.email == not_superuser.email
    assert retrieved_user.is_superuser == not_superuser.is_superuser


async def test_user_repository_can_update(session: AsyncSession, not_superuser: User):

    repo = UserRepository(session)
    setattr(not_superuser, 'email', 'new_user@gmail.com')
    retrieved_user = await repo.update(not_superuser)

    assert retrieved_user.email == not_superuser.email
    assert retrieved_user.id == not_superuser.id


async def test_user_repository_can_delete(session: AsyncSession, not_superuser: User):

    repo = UserRepository(session)
    retrieved_user = await repo.delete(not_superuser)

    res = await session.execute(select(User).filter(User.email == not_superuser.email))
    user = res.scalar_one_or_none()

    assert retrieved_user is None
    assert user is None


async def test_get_users_list(session: AsyncSession, superuser):
    users_list = [superuser]
    repo = UserRepository(session)
    retrieved_users = await repo.list(limit=2, start=0)

    assert len(retrieved_users) == 1
    for ind, obj_name in enumerate(retrieved_users):
        assert obj_name.email == users_list[ind].email
        assert obj_name.is_superuser == users_list[ind].is_superuser


async def test_user_repository_can_create(session: AsyncSession):

    new_user = User(
        email="user3@gmail.com",
        hashed_password=HashingMixin().get_password_hash('user_3')
    )
    repo = UserRepository(session)
    user = await repo.create(new_user)

    assert user.email == new_user.email
    assert user.is_superuser is False
