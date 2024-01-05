from typing import Annotated
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

str_30 = Annotated[str, 30]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}