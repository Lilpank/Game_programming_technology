from pydantic import BaseModel, ValidationError


class data_json(BaseModel):
    card: str
    get: str
    went: str