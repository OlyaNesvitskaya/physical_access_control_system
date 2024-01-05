from typing import Optional, List
from fastapi import APIRouter, Depends
from starlette import status
from services import EmployeeService
from core.current_user_depends import get_current_user
from schemas.employee_schema import *


employee_router = APIRouter(
    prefix="/employees", tags=["Employee"], dependencies=[Depends(get_current_user)]
)


@employee_router.get("", response_model=List[EmployeePostSchema])
async def get_all_employee(
        page_size: Optional[int] = 10,
        start_index: Optional[int] = 0,
        employee_service: EmployeeService = Depends()
):
    return await employee_service.list(page_size, start_index)


@employee_router.get("/{employee_id}", response_model=EmployeePostSchema)
async def get_employee(
        employee_id: int,
        employee_service: EmployeeService = Depends()
):
    return await employee_service.get(employee_id)


@employee_router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
        employee_id: int,
        employee_service: EmployeeService = Depends()
):
    await employee_service.delete(employee_id)


@employee_router.patch("/{employee_id}", response_model=EmployeePostSchema)
async def update_employee(
        employee_id: int,
        employee: UpdateEmployeeSchema,
        employee_service: EmployeeService = Depends()
):
    return await employee_service.update(employee_id, employee)


@employee_router.post("", response_model=EmployeePostSchema)
async def create_employee(
        employee: EmployeeSchema,
        employee_service: EmployeeService = Depends()
):
    return await employee_service.create(employee)


@employee_router.get("/{employee_id}/devices")
async def get_devices(
        employee_id: int,
        employee_service: EmployeeService = Depends()
):
    return await employee_service.get_devices(employee_id)
