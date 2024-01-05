from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    name: str


class DepartmentPostSchema(DepartmentSchema):
    id: int
