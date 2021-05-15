from models.data.game import GameModel, CREATE_WORKER, CREATE_WARRIOR, CREATE_FINISH_STEP, CREATE_WAR_STEP
from models.game.player import Player

__all__ = ('GameController',)


class GameController:
    """Контроллер, отвечающий за логику с игроками на стороне сервера.
    """

    def __init__(self):
        self.model = GameModel(players=dict())

    def delegate_gen_player_id(self) -> int:
        return self.model.players_count() + 1

    def check_start_game(self) -> bool:
        """Проверка, что все игроки готовы.
        """
        if self.model.players_count() > 1:
            for _, player in self.model.players.items():
                if not player.is_started:
                    return False
            return True

        return False

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

        if action == CREATE_WORKER:
            player.buy_worker()
        elif action == CREATE_WARRIOR:
            player.buy_warrior()
        # elif action == CREATE_WAR_STEP:
        #     pass
        # elif action == CREATE_FINISH_STEP:
        #     pass
        else:
            raise Exception('Игроку непозволено использовать другие события.')

        player.has_stepped = True
