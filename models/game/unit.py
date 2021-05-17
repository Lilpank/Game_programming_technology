import pydantic
import constants


class BaseGameUnit(pydantic.BaseModel):
    price: int = 5
    type: int


class Warrior(BaseGameUnit):
    price: int = 2
    type: int = constants.IS_WARRIOR


class Worker(BaseGameUnit):
    price: int = 1
    type: int = constants.IS_WORKER
