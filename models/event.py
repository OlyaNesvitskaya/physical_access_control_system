from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base_model import Base


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    success: Mapped[bool] = mapped_column(default=False)


