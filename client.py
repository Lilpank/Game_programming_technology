import logging
import typing

import pygame

from constants import CLIENT_STARTED, CLIENT_AWAIT, PLAYER_BUY_WORKER, PLAYER_BUY_WARRIOR, PLAYER_FINISH_STEP, \
    PLAYER_ACTION_ATTACK
from models.data.game import GameModel
from models.game.player import Player
from network import Network
from views.buttons import Button
from views.statistics import Statistics

pygame.font.init()
pygame.init()

size_main_window = (1200, 800)

Name_Game = "Card_game"

sc = pygame.display.set_mode(size_main_window)
pygame.display.set_caption(Name_Game)

bg_surf = pygame.image.load("Picture/menu1.JPG").convert()
sc.blit(bg_surf, (0, 0))

clock = pygame.time.Clock()
FPS = 30
pygame.display.update()

connection = Network()
player = Player.parse_raw(connection.get_pos())
is_client_send_started: bool = False


def _buy_worker_callback():
    connection.send_and_get(PLAYER_BUY_WORKER)


def _buy_warrior_callback():
    connection.send_and_get(PLAYER_BUY_WARRIOR)


def _action_attack_callback():
    connection.send_and_get(PLAYER_ACTION_ATTACK)


def _finish_step_callback():
    connection.send_and_get(PLAYER_FINISH_STEP)


buttons = [
    Button("Рабочий", 467, 600, (255, 0, 0), callback=_buy_worker_callback),
    Button("Воин", 667, 600, (0, 255, 0), callback=_buy_warrior_callback),
    Button("Атака", 867, 600, (0, 0, 250), callback=_action_attack_callback),
    Button("Закончить ход", 967, 300, (0, 0, 250), callback=_finish_step_callback)
]

# stats = [Statistics("Монеток: " + game.get_coins1(), 0, 0, (0, 0, 0)),
#          Statistics("Войнов: " + game.get_warrior1(), 0, 50, (0, 0, 0)),
#          Statistics("Рабочих: " + game.get_worker1(), 0, 100, (0, 0, 0))]


# def redraw_stat(sc, game, p):
#     if p == 0:
#         stats = [Statistics("Монеток: " + game.get_coins1(), 0, 0, (0, 0, 0)),
#                  Statistics("Войнов: " + game.get_warrior1(), 0, 50, (0, 0, 0)),
#                  Statistics("Рабочих: " + game.get_worker1(), 0, 100, (0, 0, 0))]
#         for stat in stats:
#             stat.draw(sc)
#     else:
#         stats = [Statistics("Монеток: " + game.get_coins2(), 0, 0, (0, 0, 0)),
#                  Statistics("Войнов: " + game.get_warrior2(), 0, 50, (0, 0, 0)),
#                  Statistics("Рабочих: " + game.get_worker2(), 0, 100, (0, 0, 0))]
#         for stat in stats:
#             stat.draw(sc)


def draw_await_players(layer: pygame.display) -> None:
    """Отрисовка слоя для ожидания игрока.

    :return: None.
    """
    layer.blit(pygame.image.load("Picture/BackGround.jpg").convert(), (0, 0))
    font = pygame.font.SysFont("comicsans", 80)
    text = font.render("Подождите напарника для игры", 1, (255, 0, 0), True)
    layer.blit(
        text,
        (
            size_main_window[0] / 2 - text.get_width() / 2,
            size_main_window[1] / 2 - text.get_height() / 2
        )
    )


def draw_war_place(layer: pygame.display) -> None:
    """Отрисовка поля основной игры.

    :return: None.
    """

    layer.blit(pygame.image.load("Picture/BackGround.jpg").convert(), (0, 0))
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Вы", 1, (0, 255, 255))
    layer.blit(text, (467, 450))
    # redraw_stat(sc, game, player)
    text = font.render("Соперник", 1, (0, 255, 255))
    layer.blit(text, (467, 20))
    for btn in buttons:
        btn.draw(sc)


def player_processing():
    # if game.p1Went:
    #     if game.get_player_move(0)[0] == "Р" or game.get_player_move(0)[0] == "В":
    #         game.choose_card1()
    #         redraw_stat(sc, game, player_position)
    #     if game.get_player_move(0)[0] == "З":
    #         is_next_round1 = True
    #     elif game.get_player_move(0)[0] == "А":
    #         is_fight1 = True
    #     else:
    #         try:
    #             game = network.send("reset1")
    #         except Exception as e:
    #             logging.error(e)
    #             print("Couldn't get game")
    #             return None
    #         is_next_round1 = False
    #
    # if game.p2Went:
    #     if game.get_player_move(1)[0] == "Р" or game.get_player_move(1)[0] == "В":
    #         game.choose_card2()
    #     if game.get_player_move(1)[0] == "З":
    #         is_next_round2 = True
    #     elif game.get_player_move(1)[0] == "А":
    #         is_fight2 = True
    #     else:
    #         try:
    #             game = network.send("reset2")
    #         except Exception as e:
    #             logging.error(e)
    #             print("Couldn't get game")
    #             return None
    #         is_next_round2 = False
    #
    # if is_next_round1 and is_next_round2:
    #     game.builder_mines()
    #     Game.match += 1
    #     pygame.time.delay(500)
    #
    # if is_fight1 or is_fight2:
    #     if game.p1Went and game.p2Went:
    #         if (game.is_winner() == 1 and player_position == 1) or (game.is_winner() == 0 and player_position == 0):
    #             text = font.render("Вы выйграли!", 1, (255, 0, 0))
    #             Game.match = 1
    #             Game.coins[0] = 5
    #             Game.worker[0] = 5
    #             Game.warrior[0] = 1
    #
    #             Game.coins[1] = 5
    #             Game.worker[1] = 5
    #             Game.warrior[1] = 1
    #         else:
    #             text = font.render("Вы проиграли", 1, (255, 0, 0))
    #             Game.match = 1
    #             Game.coins[0] = 5
    #             Game.worker[0] = 5
    #             Game.warrior[0] = 1
    #
    #             Game.coins[1] = 5
    #             Game.worker[1] = 5
    #             Game.warrior[1] = 1
    #
    #         sc.blit(
    #             text,
    #             (
    #                 size_main_window[0] / 2 - text.get_width() / 2,
    #                 size_main_window[1] / 2 - text.get_height() / 2
    #             )
    #         )
    #
    #         pygame.display.update()
    #         pygame.time.delay(3000)
    # redraw_window(sc, game, player_position)
    #
    # if game.both_went():
    #     redraw_window(sc, game, player_position)
    #     try:
    #         game = network.send("reset")
    #     except Exception as e:
    #         logging.error(e)
    #         print("Couldn't get game")
    #         return None
    #     pygame.display.update()

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         sys.exit()
    #
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         pos = pygame.mouse.get_pos()
    #         # for btn in btns:
    #         # if btn.click(pos) and game.connected():
    #         # if player_position == 0:
    #         #     # if not game.p1Went:
    #         #     #     network.send(btn.text)
    #         # else:
    #         #     if not game.p2Went:
    #         #         network.send(btn.text)
    pass


def main():
    global is_client_send_started, sc, player

    model = None
    try:
        if is_client_send_started:
            model: typing.Any = connection.send_and_get(CLIENT_STARTED)
            is_client_send_started = None
        elif is_client_send_started is None:
            model = connection.send_and_get(CLIENT_AWAIT)

    except ConnectionResetError:
        connection.disconnect()
        # Добавить отрисовку начального экрана с уведомлением, что соединение разорвано.
        return None

    except Exception as e:
        logging.exception(e)
        print("Couldn't get game")
        # Завершаем работу, если есть какая-то ошибка при инициализации.
        return None

    if not model:
        return None

    model_type = type(model)

    if model_type is Player:
        # Отображаем ожидание другого игрока.
        player = model
        draw_await_players(sc)
    elif model_type is GameModel:
        # Отображаем экран игры.
        draw_war_place(sc)
    # elif model_type is AlertModel:
    # Модель данных для оповещения каких-либо предупреждений клиенту.


is_running = True
while is_running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = True
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 300 < pygame.mouse.get_pos()[0] < 900 and 200 < pygame.mouse.get_pos()[1] < 400:
                    if is_client_send_started is not None and not is_client_send_started:
                        is_client_send_started = True

        for button in buttons:
            button.handle_event(event)

    main()
    pygame.display.update()
