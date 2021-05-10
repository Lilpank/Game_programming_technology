from pydantic import BaseModel, ValidationError


class data_json(BaseModel):
    warrior: (str, str)
    get: str
    went: (str, str)

