from pydantic import BaseModel, ValidationError
from models.game.player import Player
import typing

__all__ = (
    'GameModel', 'CREATE_WARRIOR', 'CREATE_WORKER',
    'CREATE_WAR_STEP', 'CREATE_FINISH_STEP',
)

CREATE_WARRIOR = 0  # Событие на создание юнита.
CREATE_WORKER = 1  # Событие на создание юнита.
CREATE_WAR_STEP = 2  # Событие на объявление войны.
CREATE_FINISH_STEP = 3  # Событие о завершении своего хода.


class GameModel(BaseModel):
    """Дата-класс.
    """

    players: dict[int, Player]

    def encoding(self) -> bytes:
        return bytes(self.json(), 'utf8')

    def players_count(self) -> int:
        return len(self.players)


class Response(BaseModel):
    """Дата-класс для взаимодействия клиента и сервера, общая обертка.
    """
    """
    data_class = 1 - Модель GameRoom
    data_class = 2 - Модель Player
    data_class = 3 - Модель GameModel
    """

    data_class: int
    data: typing.Any

