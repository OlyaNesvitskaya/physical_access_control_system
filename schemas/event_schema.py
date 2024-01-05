from pydantic import BaseModel


class EventPostSchema(BaseModel):

    entry: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'Entry': 'Admission are permitted'

                }
            ]
        }
    }