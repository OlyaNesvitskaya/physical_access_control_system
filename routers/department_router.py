from typing import Optional, List
from fastapi import APIRouter, Depends
from starlette import status

from services import DepartmentService
from core.current_user_depends import get_current_user
from schemas.department_schema import *


department_router = APIRouter(
    prefix="/departments", tags=["Department"], dependencies=[Depends(get_current_user)]
)


@department_router.get("",  response_model=List[DepartmentPostSchema])
async def get_all_department(
        page_size: Optional[int] = 10,
        start_index: Optional[int] = 0,
        department_service: DepartmentService = Depends()
):
    return await department_service.list(page_size, start_index)


@department_router.get("/{department_id}", response_model=DepartmentPostSchema)
async def get_department(
        department_id: int,
        department_service: DepartmentService = Depends()
):
    return await department_service.get(department_id)


@department_router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
        department_id: int,
        department_service: DepartmentService = Depends()
):
    await department_service.delete(department_id)


@department_router.patch("/{department_id}", response_model=DepartmentPostSchema)
async def update_department(
        department_id: int,
        department_body: DepartmentSchema,
        department_service: DepartmentService = Depends()
):
    return await department_service.update(department_id, department_body)


@department_router.post("", response_model=DepartmentPostSchema)
async def create_department(
        department: DepartmentSchema,
        department_service: DepartmentService = Depends()
):
    return await department_service.create(department)






