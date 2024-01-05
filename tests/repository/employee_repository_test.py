import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from sqlalchemy import select
from models import Employee, Department
from repository import EmployeeRepository

pytestmark = pytest.mark.anyio


async def test_get_by_card_id(session: AsyncSession, employee: Employee):

    repo = EmployeeRepository(session)
    retrieved_employee = await repo.get_by_card_id(card_id=employee.card_id)

    assert retrieved_employee.name == employee.name
    assert retrieved_employee.surname == employee.surname
    assert retrieved_employee.department_id == employee.department_id
    assert retrieved_employee.card_start_date == employee.card_start_date
    assert retrieved_employee.card_finish_date == employee.card_finish_date


async def test_employee_repository_can_get(session: AsyncSession, employee: Employee):

    repo = EmployeeRepository(session)
    retrieved_employee = await repo.get(employee.id)

    assert retrieved_employee
    assert retrieved_employee.name == employee.name
    assert retrieved_employee.surname == employee.surname
    assert retrieved_employee.department_id == employee.department_id
    assert retrieved_employee.card_id == employee.card_id


async def test_employee_repository_can_update(session: AsyncSession, employee: Employee):

    repo = EmployeeRepository(session)

    setattr(employee, 'name', 'Vasilisa')
    setattr(employee, 'card_id', 22222222)

    retrieved_employee = await repo.update(employee)

    assert retrieved_employee.name == employee.name
    assert retrieved_employee.surname == employee.surname
    assert retrieved_employee.department_id == employee.department_id
    assert retrieved_employee.card_id == employee.card_id


async def test_employee_repository_can_delete(session: AsyncSession, employee: Employee):

    repo = EmployeeRepository(session)
    retrieved_employee = await repo.delete(employee)

    res = await session.execute(select(Employee).filter(Employee.name == employee.name))
    employee = res.scalar_one_or_none()

    assert retrieved_employee is None
    assert employee is None


async def test_get_employees_list(session: AsyncSession, department: Department):

    employees_list = [
        Employee(name='Anna', surname='Karenina',
                 department_id=1, card_id=11111111,
                 card_start_date=datetime.today(), card_finish_date=datetime.today()),

        Employee(name='Jane', surname='Austen',
                 department_id=1, card_id=2222222,
                 card_start_date=datetime.today(), card_finish_date=datetime.today()),
    ]

    session.add_all(employees_list)
    await session.commit()

    repo = EmployeeRepository(session)
    retrieved_employees = await repo.list(limit=2, start=0)

    assert len(retrieved_employees) == 2
    for ind, obj_name in enumerate(retrieved_employees):
        assert obj_name.name == employees_list[ind].name


async def test_employee_repository_can_create(session: AsyncSession, department: Department):

    new_employee = Employee(name='Aleksander', surname='Pushkin',
                            department_id=department.id, card_id=3333333,
                            card_start_date=datetime.today(), card_finish_date=datetime.today())

    repo = EmployeeRepository(session)
    retrieved_employee = await repo.create(new_employee)

    assert retrieved_employee.name == new_employee.name
    assert retrieved_employee.surname == new_employee.surname
    assert retrieved_employee.department_id == new_employee.department_id
    assert retrieved_employee.card_id == new_employee.card_id
    assert retrieved_employee.card_start_date == date.today()
    assert retrieved_employee.card_finish_date == date.today()



