from datetime import date, timedelta
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base_model import Base, str_30
from .access_control_table import access_control_table


class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        CheckConstraint('card_finish_date >= card_start_date'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_30] = mapped_column(nullable=False)
    surname: Mapped[str_30] = mapped_column(nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    card_id: Mapped[int] = mapped_column(unique=True)
    card_start_date: Mapped[date] = mapped_column(default=date.today)
    card_finish_date: Mapped[date] = mapped_column(default=date.today() + timedelta(days=1))
    devices: Mapped[list["Device"]] = relationship(
        "Device", secondary=access_control_table, back_populates='employees'
    )

