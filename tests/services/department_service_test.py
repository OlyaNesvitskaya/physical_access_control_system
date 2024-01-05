import pytest
from fastapi import HTTPException
from services import DepartmentService
from schemas.department_schema import DepartmentSchema

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    'page_size, start_index, number_of_records',
    [
        (3, 0, 3),
        (0, 0, 0),
        (5, 1, 2)
    ]
)
async def test_list(page_size, start_index, number_of_records, fake_department_repository):

    retrieved = await DepartmentService(fake_department_repository).list(page_size=page_size, start_index=start_index)

    assert len(retrieved) == number_of_records


async def test_get(fake_department_repository):

    first_department = fake_department_repository.items[0]
    retrieved = await DepartmentService(fake_department_repository).get(first_department.id)

    assert retrieved.id == first_department.id
    assert retrieved.name == first_department.name


async def test_error_get(fake_department_repository):

    with pytest.raises(HTTPException) as excinfo:
        await DepartmentService(fake_department_repository).get(100)

    assert excinfo.type is HTTPException


async def test_update(fake_department_repository):

    first_department = fake_department_repository.items[0]
    retrieved = await (DepartmentService(fake_department_repository)
                       .update(first_department.id, DepartmentSchema(name='dep_22222')))

    assert retrieved.id == first_department.id
    assert retrieved.name == 'dep_22222'


@pytest.mark.parametrize(
    'department_id, department_body, type_exception, exception_value',
    [
        (2, DepartmentSchema(name='new_department3'), HTTPException,
         "(409, 'Department with name:new_department3 already exist.')"),

        (100, DepartmentSchema(name='dep_22222'), HTTPException,
         "(400, 'Department with supplied ID does not exist.')"),
    ]
)
async def test_error_update(department_id, department_body, fake_department_repository,
                            type_exception, exception_value):

    with pytest.raises(type_exception) as excinfo:
        await DepartmentService(fake_department_repository).update(department_id, department_body)

    assert excinfo.type is type_exception
    assert str(excinfo.value) == exception_value


async def test_create(fake_department_repository):

    new_department = DepartmentSchema(id=5, name='new_department')
    retrieved = await DepartmentService(fake_department_repository).create(new_department)

    assert retrieved.name == new_department.name


async def test_error_create(fake_department_repository):

    with pytest.raises(HTTPException) as excinfo:
        await DepartmentService(fake_department_repository).create(DepartmentSchema(id=5, name='new_department'))

    assert excinfo.type is HTTPException


async def test_delete(fake_department_repository):

    retrieved = await (DepartmentService(fake_department_repository)
                       .delete(fake_department_repository.items[-1].id))

    assert retrieved is None


async def test_error_delete(fake_department_repository):

    with pytest.raises(HTTPException) as excinfo:
        await DepartmentService(fake_department_repository).delete(100)

    assert excinfo.type is HTTPException


