from typing import List, Optional, Sequence
from fastapi import Depends
from sqlalchemy import exc

from models import Device, Employee
from repository import DeviceRepository, DepartmentRepository, EmployeeRepository
from schemas.device_schema import DeviceSchema, UpdateDeviceSchema, DeviceEmployeePostRequestSchema
from exc import raise_with_log


class DeviceService:
    department_repository: DepartmentRepository
    device_repository: DeviceRepository
    employee_repository: EmployeeRepository

    def __init__(
        self,
        device_repository: DeviceRepository = Depends(),
        department_repository: DepartmentRepository = Depends(),
        employee_repository: EmployeeRepository = Depends()

    ) -> None:
        self.device_repository = device_repository
        self.department_repository = department_repository
        self.employee_repository = employee_repository

    async def create(
        self, device_body: DeviceSchema
    ) -> Device:

        device_body = device_body.model_dump()
        await self.__check_if_exist_department_id(device_body)

        try:
            return await self.device_repository.create(
                Device(**device_body)
            )
        except exc.IntegrityError as e:
            raise_with_log(status_code=409,
                           detail=f"Employee with card_id:{device_body['imei']} already exist.")

    async def delete(
        self, device_id: int
    ) -> None:

        device = await self.get(device_id, bound_employees=True)
        device.employees = []
        await self.device_repository.delete(device)

    async def get(
        self, device_id: int, bound_employees=False
    ) -> Device:
        device = await self.device_repository.get(device_id, bound_employees)
        if not device:
            raise_with_log(status_code=400, detail="Device with supplied ID does not exist.")
        return device

    async def list(
        self, page_size: Optional[int] = 100, start_index: Optional[int] = 0,
    ) -> Sequence[Device]:
        return await self.device_repository.list(page_size, start_index)

    async def update(
        self, device_id: int, device_body: UpdateDeviceSchema
    ) -> Device:
        device = await self.get(device_id)
        device_body = device_body.model_dump(exclude_unset=True)
        if "department_id" in device_body:
            await self.__check_if_exist_department_id(device_body)
        for key, value in device_body.items():
            setattr(device, key, value)

        try:
            return await self.device_repository.update(device)
        except exc.IntegrityError as e:
            raise_with_log(status_code=409,
                           detail=f"Device with imei:{device_body['imei']} already exist.")

    async def __check_if_exist_department_id(self, device_body):
        """
            Сhecking the existence of a department.
        """

        is_department_id_exist = await self.department_repository.get(device_body.get("department_id"))
        if not is_department_id_exist:
            raise_with_log(status_code=400,
                           detail="Incorrect department_id. Department with supplied ID does not exist.")

    async def get_employees(self, device_id: int) -> List[Employee]:
        """
            Obtaining a list of employees who are given the opportunity to enter through this device.
        """

        employees_list = await self.device_repository.get(
            device_id, True
        )
        return employees_list.employees

    async def add_employee(self, body: DeviceEmployeePostRequestSchema) -> None:
        """
            Adding an employee to gain access to the device.
        """

        employee = await self.employee_repository.get(body.employee_id)
        device = await self.device_repository.get(body.device_id, True)

        if not employee or not device:
            raise_with_log(status_code=400,
                           detail="Incorrect employee_id or device_id")

        try:
            device.employees.append(employee)
            await self.device_repository.update(device)
        except exc.IntegrityError as e:
            raise_with_log(status_code=409,
                           detail=f"Employee already has access to this device!")

    async def remove_employee(self, device_id: int, employee_id: int) -> None:
        """
            Take away access to the device from the specified employee.
        """

        employee = await self.employee_repository.get(employee_id)
        device = await self.device_repository.get(device_id, True)

        if not employee or not device:
            raise_with_log(status_code=400,
                           detail="Incorrect employee_id or device_id")

        device.employees = list(filter(
            lambda employee: employee.id != employee_id,
            device.employees,
        ))

        await self.device_repository.update(device)



