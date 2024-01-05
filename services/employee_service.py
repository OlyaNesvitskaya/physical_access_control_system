from typing import Optional, Sequence
from fastapi import Depends, HTTPException
from sqlalchemy import exc

from models import Employee
from repository import EmployeeRepository, DepartmentRepository
from schemas.employee_schema import EmployeeSchema, UpdateEmployeeSchema
from exc import raise_with_log


class EmployeeService:
    department_repository: DepartmentRepository
    employee_repository: EmployeeRepository

    def __init__(
        self,
        employee_repository: EmployeeRepository = Depends(),
        department_repository: DepartmentRepository = Depends()
    ) -> None:
        self.employee_repository = employee_repository
        self.department_repository = department_repository

    async def create(
        self, employee_body: EmployeeSchema
    ) -> Employee:

        employee_body = employee_body.model_dump()
        await self.__check_if_exist_department_id(employee_body)

        try:
            return await self.employee_repository.create(
                Employee(**employee_body)
            )
        except exc.IntegrityError as e:
            raise HTTPException(status_code=409,
                                detail=f"Employee with card_id:{employee_body['card_id']} already exist.")

    async def delete(
        self, employee_id: int
    ) -> None:

        employee = await self.get(employee_id, bound_employees=True)
        employee.devices = []

        await self.employee_repository.delete(employee)

    async def get(
        self, employee_id: int, bound_employees=False
    ) -> Employee:

        employee = await self.employee_repository.get(employee_id, bound_employees)

        if not employee:
            raise_with_log(status_code=400,
                           detail="Employee with supplied ID does not exist.")

        return employee

    async def list(
        self, page_size: Optional[int] = 100, start_index: Optional[int] = 0,
    ) -> Sequence[Employee]:

        return await self.employee_repository.list(page_size, start_index)

    async def update(
        self, employee_id: int, employee_body: UpdateEmployeeSchema
    ) -> Employee:

        employee = await self.get(employee_id)
        employee_body = employee_body.model_dump(exclude_unset=True)

        if "department_id" in employee_body:
            await self.__check_if_exist_department_id(employee_body)

        for key, value in employee_body.items():
            setattr(employee, key, value)

        try:
            return await self.employee_repository.update(employee)
        except exc.IntegrityError as e:
            error = e.orig.args[0].lower()

            if "check" in error:
                raise_with_log(status_code=400,
                               detail=f"Card_finish_date must be bigger or equal card_start_date.")

            if "unique" in error:
                raise_with_log(status_code=409,
                               detail=f"Employee with card_id:{employee_body['card_id']} already exist.")

            raise_with_log(status_code=400, detail=error)

    async def __check_if_exist_department_id(self, employee_body):
        if_department_id_exist = await (self.department_repository.
                                        get(employee_body.get("department_id")))
        if not if_department_id_exist:
            raise_with_log(status_code=400,
                           detail="Incorrect department_id. Department with supplied ID does not exist.")

    async def get_devices(self, employee_id: int) -> Employee | None:
        """
           Obtaining a list of available devices for employee.
        """
        result = await self.employee_repository.get(
            employee_id, bound_devices=True
        )
        return result.devices

