import enum
from pydantic import BaseModel


class RouteEnum(str, enum.Enum):
    enter = "enter"
    exit = "exit"


class DeviceSchema(BaseModel):
    imei: str
    department_id: int
    name: str
    opened: bool = False
    route: RouteEnum

    class Config:
        use_enum_values = True


class DevicePostSchema(DeviceSchema):
    id: int


class UpdateDeviceSchema(BaseModel):
    imei: str | None = None
    department_id: int | None = None
    name: str | None = None
    opened: bool | None = None
    route: RouteEnum | None = None

    class Config:
        use_enum_values = True


class DeviceEmployeePostRequestSchema(BaseModel):
    device_id: int
    employee_id: int
