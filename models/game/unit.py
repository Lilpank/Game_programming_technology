import pydantic
import constants


class BaseGameUnit(pydantic.BaseModel):
    price: int = 5
    type: int


class Warrior(BaseGameUnit):
    price: int = constants.PRICE_WARRIOR
    type: int = constants.IS_WARRIOR


class Worker(BaseGameUnit):
    price: int = constants.PRICE_WORKER
    type: int = constants.IS_WORKER
