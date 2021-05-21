from models.data.game import GameModel, CREATE_WORKER, CREATE_WARRIOR, CREATE_FINISH_STEP, CREATE_WAR_STEP
from models.game.player import Player
from random import shuffle
from models.data.room import GameRoom
import typing

__all__ = ('GameController',)


class GameController:
    """Контроллер, отвечающий за логику с игроками на стороне сервера.
    """

    def __init__(self):
        self.model = GameModel(players=dict())
        self.rooms: list[GameRoom] = list()

    def get_room(self, player_id) -> typing.Optional[GameRoom]:
        for room in self.rooms:
            if player_id in room.get_contains_players():
                return room

        return None

    def delegate_gen_player_id(self) -> int:
        return self.model.players_count() + 1

    def check_start_game(self) -> bool:
        """Проверка, что все игроки готовы.
        """
        count = 0
        if self.model.players_count() > 1:
            for _, player in self.model.players.items():
                count += 1 if player.is_started else 0
        return count >= 2

    def add_player(self, player: Player) -> None:
        self.model.players.update({player.id: player})
        print(f'Player #{player.id} has been added.')

    def remove_player(self, player: Player) -> None:
        try:
            del self.model.players[player.id]
            print(f'Player #{player.id} has been removed.')
        except Exception as e:
            print(e)

    def reset(self):
        for _, player in self.model.players:
            player.is_started = False

    def player_action(self, player_id: int, action: int) -> None:
        player = self.model.players[player_id]
        room = self.get_room(player_id)

        if action == CREATE_WORKER:
            player.buy_worker()
        elif action == CREATE_WARRIOR:
            player.buy_warrior()
        elif action == CREATE_WAR_STEP:
            player.is_attacked = True
            if room:
                room.player_passed(player)
                if room.round_finished():
                    room.player_defender()
        elif action == CREATE_FINISH_STEP:
            if room:
                room.player_passed(player)
                if room.round_finished():
                    if room.is_attacked():
                        room.player_defender()
                    room.new_round()


        else:
            raise Exception('Игроку непозволено использовать другие события.')

        player.has_stepped = True

    def chunk_active_players(self, exclude: list[int]) -> typing.Optional[list[Player]]:
        if self.model.players is None:
            return None

        players = list(filter(lambda x: x.is_started and x.id not in exclude, self.model.players.values()))
        if len(players) <= 1:
            raise Exception

        shuffle(players)
        return players[:2]
