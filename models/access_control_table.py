from sqlalchemy import ForeignKey, Column
from sqlalchemy import Table
from models.base_model import Base


access_control_table = Table(
    "access_control_table",
    Base.metadata,
    Column("employee_id", ForeignKey("employees.id", ondelete='CASCADE'), primary_key=True),
    Column("device_id", ForeignKey("devices.id", ondelete='CASCADE'), primary_key=True),
)






