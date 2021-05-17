import pydantic
from typing import Any, Optional
from models.game.unit import BaseGameUnit, Worker, Warrior
import constants


class NotHaveMoney(Exception):
    pass


class Player(pydantic.BaseModel):
    """Идентификатор игрока.
    """
    id: int

    """Готов к игре.
    """
    is_started: bool = False

    """Игрок в процессе игры.
    """
    is_gaming: bool = False

    """Сделал свой ход.
    """
    has_stepped: bool = False

    """Кол-во монет у игрока.
    """
    coins: int = 5

    """Юниты у игрока.
    """
    units: list[Any] = []

    """Завершил свой матч.
    """
    has_finish_step: bool = False

    def _add_unit(self, model: BaseGameUnit):
        self.units.append(model)

    def get_units(self) -> Optional[list]:
        def mapper(item):
            if item is None:
                raise Exception()

            if hasattr(item, 'type'):
                return item
            else:
                if item['type'] == constants.IS_WORKER:
                    obj = Worker(**item)
                elif item['type'] == constants.IS_WARRIOR:
                    obj = Warrior(**item)
                else:
                    raise Exception()
            return obj

        return list(map(mapper, self.units))

    def get_worker_count(self) -> int:
        if not self.get_units():
            return 0
        return len(list(filter(lambda x: type(x) is Worker, self.get_units())))

    def get_warrior_count(self) -> int:
        if not self.get_units():
            return 0
        return len(list(filter(lambda x: type(x) is Warrior, self.get_units())))

    def get_coins_count(self) -> int:
        return self.coins

    def buy_worker(self) -> None:
        if self.coins < Worker().price:
            raise NotHaveMoney()

        self.coins -= Worker().price
        self._add_unit(Worker())

    def buy_warrior(self) -> None:
        if self.coins < Warrior().price:
            raise NotHaveMoney()

        self.coins -= Warrior().price
        self._add_unit(Warrior())

    def coins_increase(self):
        self.coins += self.get_worker_count()
