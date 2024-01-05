from typing import Optional, List
from fastapi import APIRouter, Depends
from starlette import status

from services import DeviceService
from schemas.device_schema import *
from core.current_user_depends import get_current_user

device_router = APIRouter(
    prefix="/devices", tags=["Device"], dependencies=[Depends(get_current_user)]
)


@device_router.get("", response_model=List[DevicePostSchema])
async def get_all_devices(
        page_size: Optional[int] = 10,
        start_index: Optional[int] = 0,
        device_service: DeviceService = Depends()
):
    return await device_service.list(page_size, start_index)


@device_router.get("/{device_id}", response_model=DevicePostSchema)
async def get_device(
        device_id,
        device_service: DeviceService = Depends()
):
    return await device_service.get(device_id)


@device_router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
        device_id: int,
        device_service: DeviceService = Depends()
):
    await device_service.delete(device_id)


@device_router.patch("/{device_id}", response_model=DevicePostSchema)
async def update_device(
        device_id: int,
        device: UpdateDeviceSchema,
        device_service: DeviceService = Depends()
):
    return await device_service.update(device_id, device)


@device_router.post("", response_model=DevicePostSchema)
async def create_device(
        device: DeviceSchema,
        device_service: DeviceService = Depends()
):
    return await device_service.create(device)


@device_router.get("/{device_id}/employees")
async def get_employees(
        device_id: int,
        device_service: DeviceService = Depends()
):
    return await device_service.get_employees(device_id)


@device_router.post("/access", status_code=status.HTTP_204_NO_CONTENT)
async def provide_employee_access_to_device(
        body: DeviceEmployeePostRequestSchema,
        device_service: DeviceService = Depends()
):
    await device_service.add_employee(body)


@device_router.delete("/{device_id}/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def forbid_employee_access_to_device(
        device_id: int,
        employee_id: int,
        device_service: DeviceService = Depends()
):
    await device_service.remove_employee(device_id, employee_id)


