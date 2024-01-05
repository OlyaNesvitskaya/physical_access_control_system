import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Department
from repository import DepartmentRepository


pytestmark = pytest.mark.anyio


async def test_department_repository_can_get(session: AsyncSession, department: Department):

    retrieved_department = await DepartmentRepository(session).get(department.id)

    assert retrieved_department.name == department.name


async def test_department_repository_can_update(session: AsyncSession, department: Department):

    repo = DepartmentRepository(session)
    setattr(department, 'name', 'new_dep')
    retrieved_department = await repo.update(department)

    assert retrieved_department.name == department.name
    assert retrieved_department.id == department.id


async def test_department_repository_can_delete(session: AsyncSession, department: Department):

    repo = DepartmentRepository(session)
    retrieved_department = await repo.delete(department)

    res = await session.execute(select(Department).filter(Department.name == department.name))
    department = res.scalar_one_or_none()

    assert retrieved_department is None
    assert department is None


async def test_get_departments_list(session: AsyncSession):

    departments_list = [Department(name='dep1'), Department(name='dep2')]
    session.add_all(departments_list)
    await session.commit()
    repo = DepartmentRepository(session)
    retrieved_department = await repo.list(limit=2, start=0)

    assert len(retrieved_department) == 2
    for ind, obj_name in enumerate(retrieved_department):
        assert obj_name.name == departments_list[ind].name


async def test_department_repository_can_create(session: AsyncSession):

    department = Department(name="dep3")
    repo = DepartmentRepository(session)
    department = await repo.create(department)

    assert department.name == "dep3"
