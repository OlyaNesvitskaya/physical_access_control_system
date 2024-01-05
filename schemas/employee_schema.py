from pydantic import BaseModel, model_validator
from datetime import date


class EmployeeSchema(BaseModel):

    name: str
    surname: str
    department_id: int
    card_start_date: date
    card_finish_date: date
    card_id: int

    @model_validator(mode='after')
    def check_date(self):
        if self.card_finish_date < self.card_start_date:
            raise ValueError('Card_finish_date must be bigger or equal card_start_date')
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "name": "Jane",
                "surname": "Austen",
                "department_id": 1,
                "card_start_date": "2024-01-06",
                "card_finish_date": "2024-01-06",
                "card_id": 111111
                }
            ]
        }
    }


class UpdateEmployeeSchema(BaseModel):

    name: str | None = None
    surname: str | None = None
    department_id: int | None = None
    card_start_date: date | None = None
    card_finish_date: date | None = None
    card_id: int | None = None


class EmployeePostSchema(EmployeeSchema):
    id: int

    @model_validator(mode='after')
    def check_date(self):
        return self
