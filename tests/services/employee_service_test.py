from datetime import date, timedelta
import pytest
from fastapi import HTTPException

from services import EmployeeService
from schemas.employee_schema import EmployeeSchema, UpdateEmployeeSchema

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    'page_size, start_index, number_of_records',
    [
        (3, 0, 3),
        (0, 0, 0),
        (5, 1, 2)
    ]
)
async def test_list(page_size, start_index, number_of_records, fake_employee_repository, fake_department_repository):

    retrieved = await (EmployeeService(fake_employee_repository, fake_department_repository)
                       .list(page_size=page_size, start_index=start_index))

    assert len(retrieved) == number_of_records
    assert retrieved == fake_employee_repository.items[start_index:page_size]


async def test_get(fake_employee_repository, fake_department_repository):

    first_employee = fake_employee_repository.items[0]
    retrieved = await (EmployeeService(fake_employee_repository, fake_department_repository)
                       .get(first_employee.id, False))

    assert retrieved.name == first_employee.name
    assert retrieved.surname == first_employee.surname
    assert retrieved.department_id == first_employee.department_id
    assert retrieved.card_id == first_employee.card_id


async def test_error_get(fake_employee_repository, fake_department_repository):

    with pytest.raises(HTTPException) as excinfo:
        await EmployeeService(fake_employee_repository, fake_department_repository).get(10)

    assert excinfo.type is HTTPException


async def test_update(fake_employee_repository, fake_department_repository):

    first_employee = fake_employee_repository.items[0]
    retrieved = await (EmployeeService(fake_employee_repository, fake_department_repository)
                       .update(first_employee.id, UpdateEmployeeSchema(card_id=101010)))

    assert retrieved.name == first_employee.name
    assert retrieved.surname == first_employee.surname
    assert retrieved.department_id == first_employee.department_id
    assert retrieved.card_id == first_employee.card_id


@pytest.mark.parametrize(
    'employee_id, employee_schema, type_exception, exception_value',
    [
        (1, UpdateEmployeeSchema(department_id=100), HTTPException,
            "(400, 'Incorrect department_id. Department with supplied ID does not exist.')"),

        (2, UpdateEmployeeSchema(card_id=3333333), HTTPException,
           "(409, 'Employee with card_id:3333333 already exist.')"),

        (10, UpdateEmployeeSchema(card_id=101010), HTTPException,
            "(400, 'Employee with supplied ID does not exist.')"),

        (1, UpdateEmployeeSchema(card_finish_date=date.today()-timedelta(days=2)), HTTPException,
         "(400, 'Card_finish_date must be bigger or equal card_start_date.')")
    ]
)
async def test_error_update(fake_employee_repository, fake_department_repository,
                      employee_id, employee_schema, type_exception, exception_value):

    with pytest.raises(type_exception) as excinfo:

        await EmployeeService(fake_employee_repository, fake_department_repository).update(employee_id, employee_schema)

    assert excinfo.type is type_exception
    assert str(excinfo.value) == exception_value


async def test_create(fake_employee_repository, fake_department_repository, department):

    new_employee = EmployeeSchema(
        name='Atyui', surname='Kkjml', department_id=department.id, card_id=555555,
        card_start_date=date.today(),
        card_finish_date=date.today()
    )

    retrieved = await EmployeeService(fake_employee_repository, fake_department_repository).create(new_employee)

    assert retrieved.name == new_employee.name
    assert retrieved.surname == new_employee.surname
    assert retrieved.department_id == new_employee.department_id
    assert retrieved.card_id == new_employee.card_id


async def test_error_create(fake_employee_repository, fake_department_repository):

    with pytest.raises(HTTPException) as excinfo:
        employee = EmployeeSchema(
            name='Atyui', surname='Kkjml', department_id=fake_department_repository.items[0].id, card_id=555555,
            card_start_date=date.today(),
            card_finish_date=date.today())

        await EmployeeService(fake_employee_repository, fake_department_repository).create(employee)

    assert excinfo.type is HTTPException


async def test_delete(fake_employee_repository, fake_department_repository):

    retrieved = await (EmployeeService(fake_employee_repository, fake_department_repository)
                       .delete(fake_employee_repository.items[-1].id))

    assert retrieved is None


async def test_error_delete(fake_employee_repository, fake_department_repository):

    with pytest.raises(HTTPException) as excinfo:
        await (EmployeeService(fake_employee_repository, fake_department_repository).delete(100))

    assert excinfo.type is HTTPException