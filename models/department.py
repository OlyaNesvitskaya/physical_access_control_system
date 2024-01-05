from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base_model import Base, str_30


class Department(Base):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_30] = mapped_column(nullable=False, unique=True)


