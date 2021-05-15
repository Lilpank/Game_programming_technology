import pydantic


class BaseGameUnit(pydantic.BaseModel):
    price: int = 5


class Warrior(BaseGameUnit):
    price: int = 10


class Worker(BaseGameUnit):
    price: int = 5
