from typing import Literal, get_args
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base_model import Base, str_30
from .access_control_table import access_control_table


Route = Literal["enter", "exit"]


class Device(Base):
    __tablename__ = 'devices'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_30] = mapped_column(nullable=False)
    opened: Mapped[bool] = mapped_column(default=False)
    imei: Mapped[str_30] = mapped_column(nullable=False, unique=True)
    route: Mapped[Route] = mapped_column(
        Enum(*get_args(Route),
             name="route",
             validate_strings=True))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    employees: Mapped[list["Employee"]] = relationship(
        "Employee", secondary=access_control_table, back_populates='devices'

    )

