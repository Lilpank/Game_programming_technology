import logging
import typing
import pygame
from constants import CLIENT_STARTED, CLIENT_AWAIT, PLAYER_BUY_WORKER, PLAYER_BUY_WARRIOR, PLAYER_FINISH_STEP, \
    PLAYER_ACTION_ATTACK
from models.data.game import GameModel
from models.game.player import Player
from network import Network
from views.buttons import Button
from models.data.room import GameRoom
from views.statistics import Statistics
from sprite import character
from sprite import snap

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
communication_as_json: bool = True


def _buy_worker_callback():
    connection.send_and_get(PLAYER_BUY_WORKER, player.id)


def _buy_warrior_callback():
    connection.send_and_get(PLAYER_BUY_WARRIOR, player.id)


def _action_attack_callback():
    connection.send_and_get(PLAYER_ACTION_ATTACK, player.id)


def _finish_step_callback():
    connection.send_and_get(PLAYER_FINISH_STEP, player.id)


def redraw_stat(sc, player: Player, match) -> None:
    stats = [Statistics("Количетсво кристаллов: " + str(player.coins), 400, 450, (0, 255, 255),
                        font=pygame.font.SysFont("fonts/BelweBoldBT.ttf", 45)),
             Statistics(str(player.get_warrior_count()), 415, 712, (0, 0, 0),
                        font=pygame.font.Font("fonts/BelweBoldBT.ttf", 45)
                        ),
             Statistics(str(player.get_worker_count()), 673, 711, (0, 0, 0),
                        font=pygame.font.Font("fonts/BelweBoldBT.ttf", 45)
                        )]
    for stat in stats:
        stat.draw(sc)

    font = pygame.font.SysFont('comicans', 50)
    text = font.render("Раунд " + str(match), 1, (0, 255, 255))
    sc.blit(text, (525, 300))


def screen_for_the_end_of_the_game(layer, room: GameRoom, player: Player) -> None:
    """Отрисовка экрана в конце игры.

    :param layer: Surface
    :param room: LockerRoom
    :param player: Player
    :return: None
    """

    layer.blit(pygame.image.load("Picture/BackGround.jpg").convert(), (0, 0))
    font = pygame.font.SysFont("comicsans", 80)

    if room.winner == player.id:
        text = font.render("Вы победили! :)", 1, (255, 0, 0), True)
    else:
        text = font.render("Вы проиграли! :'(", 1, (255, 0, 0), True)

    layer.blit(
        text,
        (
            size_main_window[0] / 2 - text.get_width() / 2,
            size_main_window[1] / 2 - text.get_height() / 2
        )
    )


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


characters = pygame.sprite.Group()
warrior = character.WarriorCharacter(340, 655, 'Picture/Warrior.png')
worker = character.Worker_Character(600, 650, 'Picture/Worker.png')
characters.add(warrior, worker)

snaps = pygame.sprite.Group()
snap_attack = snap.Snap(870, 650, 'Picture/act_attack.png')
snap_end_turn = snap.Snap(1050, 350, 'Picture/act_end_turn.png')
snaps.add(snap_attack, snap_end_turn)

buttons = [
    Button(505, 559, width=181, height=183,
           callback=_buy_worker_callback),
    Button(250, 557, width=186, height=190,
           callback=_buy_warrior_callback),
    Button(780, 555, width=snap_attack.image.get_width(), height=snap_attack.image.get_height(),
           callback=_action_attack_callback),
    Button(979, 309, width=snap_end_turn.image.get_width(), height=snap_end_turn.image.get_height(),
           callback=_finish_step_callback)
]


def draw_war_place(layer: pygame.display) -> None:
    """Отрисовка поля основной игры.

    :return: None.
    """
    layer.fill(0)
    layer.blit(pygame.image.load("Picture/Back_ground_fight1.jpg").convert(), (0, 0))

    characters.update(int(player.get_coins_count()))
    characters.draw(layer)

    snaps.update(player.has_finish_step)
    snaps.draw(layer)

    for btn in buttons:
        btn.draw()


def main():
    global is_client_send_started, sc, player

    model = None
    try:
        if is_client_send_started:
            model: typing.Any = connection.send_and_get(CLIENT_STARTED, player.id)
            is_client_send_started = None
        elif is_client_send_started is None:
            model = connection.send_and_get(CLIENT_AWAIT, player.id)

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
    elif model_type is GameRoom:
        room: GameRoom = model
        player = model.player_data(player.id)
        draw_war_place(sc)
        redraw_stat(sc, player, room.get_match())

        if room.winner is not None:
            screen_for_the_end_of_the_game(sc, room, player)


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
