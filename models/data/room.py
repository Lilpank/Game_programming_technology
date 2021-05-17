from models.game.player import Player
from uuid import uuid4
import pydantic

IS_WIN = 1
IS_LOSS = 0


class GameRoom(pydantic.BaseModel):
    """Класс отвечающий за количество игроков в комнате и за количество раундов.
    """
    uuid: str = uuid4()

    match: int = 1

    players: list[Player] = list()

    passed: list[int] = list()

    wins: dict[Player, int] = dict()

    def player_passed(self, player: Player):
        # TODO: Необходимо определить кому можно совершить следующий ход за раунд.
        if player.id not in self.passed:
            self.passed.append(player.id)
            player.has_finish_step = False

    def round_finished(self) -> bool:
        return len(self.passed) == 2

    def new_round(self):
        self.passed = list()
        self.match += 1
        self._coins_increase()

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

    def player_attack(self, attacker: Player):
        for player in self.players:
            if player.id != attacker.id and attacker.get_warrior_count() > player.get_warrior_count():
                self.wins.update(attacker=1, player=0)
            else:
                self.wins.update(attacker=0, player=1)
        print(self.wins)
        # self._default_values()

    def _default_values(self):
        self.match = 1
        for player in self.players:
            player.coins = 5
            player.units = 0
