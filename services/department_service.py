from typing import Optional, Sequence
from fastapi import Depends
from sqlalchemy import exc

from exc import raise_with_log
from models import Department
from repository import DepartmentRepository
from schemas.department_schema import DepartmentSchema


class DepartmentService:
    department_repository: DepartmentRepository

    def __init__(
        self, department_repository: DepartmentRepository = Depends()
    ) -> None:
        self.department_repository = department_repository

    async def create(
        self, department_body: DepartmentSchema
    ) -> Department:
        try:
            return await self.department_repository.create(
                Department(name=department_body.name)
            )
        except exc.IntegrityError as e:
            raise_with_log(409, detail=f"Department with name:{department_body.name} already exist.")

    async def delete(
        self, department_id: int
    ) -> None:
        department = await self.get(department_id)

        try:
            await self.department_repository.delete(department)
        except exc.IntegrityError as e:
            raise_with_log(409,
                           detail='This department cannot be deleted because either employees or devices belong to it')

    async def get(
        self, department_id: int
    ) -> Department | None:
        department = await self.department_repository.get(department_id)
        if not department:
            raise_with_log(status_code=400, detail="Department with supplied ID does not exist.")
        return department

    async def list(
        self, page_size: Optional[int] = 10, start_index: Optional[int] = 0,
    ) -> Sequence[Department]:
        return await self.department_repository.list(page_size, start_index)

    async def update(
        self, department_id: int, department_body: DepartmentSchema
    ) -> Department:
        department = await self.get(department_id)
        department_body = department_body.model_dump(exclude_unset=True)
        for key, value in department_body.items():
            setattr(department, key, value)

        try:
            return await self.department_repository.update(department)
        except exc.IntegrityError as e:
            raise_with_log(status_code=409,
                           detail=f"Department with name:{department_body.get('name', '')} already exist.")





