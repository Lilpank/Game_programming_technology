from typing import Optional

from models.game.player import Player
from uuid import uuid4
import pydantic


class GameRoom(pydantic.BaseModel):
    """Класс отвечающий за количество игроков в комнате и за количество раундов.
    """
    uuid: str = uuid4()

    match: int = 1

    players: list[Player] = list()

    passed: list[int] = list()

    winner: Optional[int] = None

    def player_passed(self, player: Player):
        # TODO: Необходимо определить кому можно совершить следующий ход за раунд.
        if player.id not in self.passed:
            self.passed.append(player.id)
            player.has_finish_step = False

    def round_finished(self) -> bool:
        return len(self.passed) == len(self.players)

    def new_round(self):
        self.passed = list()
        self.match += 1
        self._coins_increase()
        for player in self.players:
            player.is_attacked = False

    def set_players(self, players: list[Player]):
        self.players = players

    def get_contains_players(self) -> list[int]:
        return [x.id for x in self.players]

    def player_data(self, player_id) -> Player:
        for player in self.players:
            if player.id == player_id:
                return player

    def get_match(self) -> int:
        return self.match

    def _coins_increase(self):
        for player in self.players:
            player.coins_increase()

    def player_defender(self):
        attacked = None
        defender = None

        for player in self.players:
            if player.is_attacked:
                attacked = player
            else:
                defender = player
        if attacked.get_warrior_count() == defender.get_warrior_count():
            self.winner = defender.id
        if attacked.get_warrior_count() > defender.get_warrior_count():
            self.winner = attacked.id
        else:
            self.winner = defender.id

    def is_attacked(self) -> bool:
        return any(filter(lambda x: x.is_attacked, self.players))

    def is_apocalypse(self):
        return len(list(filter(lambda x: x.is_attacked, self.players))) == len(self.players)
