import pydantic
from models.game.unit import BaseGameUnit, Worker, Warrior


class NotHaveMoney(Exception):
    pass


class Player(pydantic.BaseModel):
    """Идентификатор игрока.
    """
    id: int

    """Готов к игре.
    """
    is_started: bool = False

    """Сделал свой ход.
    """
    has_stepped: bool = False

    """Кол-во монет у игрока.
    """
    coins: int = 5

    """Юниты у игрока.
    """
    units: list[BaseGameUnit] = []

    def _add_unit(self, model: BaseGameUnit):
        self.units.append(model)

    def get_worker_count(self) -> int:
        return len(filter(lambda x: type(x) is Worker, self.units))

    def get_warrior_count(self):
        return len(filter(lambda x: type(x) is Warrior, self.units))

    def buy_worker(self) -> None:
        if self.coins < Worker().price:
            raise NotHaveMoney()

        self._add_unit(Worker())

    def buy_warrior(self) -> None:
        if self.coins < Warrior().price:
            raise NotHaveMoney()

        self._add_unit(Warrior())
