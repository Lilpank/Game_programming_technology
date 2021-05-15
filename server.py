import socket
import logging
from _thread import *
from models.game.player import Player, NotHaveMoney
from controllers.game import GameController
from constants import HOST, PORT, CLIENT_RESET, CLIENT_STARTED, CLIENT_STEP, CLIENT_AWAIT, PLAYER_BUY_WORKER, \
    PLAYER_BUY_WARRIOR, PLAYER_ACTION_ATTACK, PLAYER_FINISH_STEP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")

game = GameController()


def threaded_client(connect: socket.socket, player: Player):
    connect.send(player.json().encode('utf8'))

    while True:
        try:
            data = connect.recv(4096).decode()
            if not data:
                break

            if data in [CLIENT_STARTED, CLIENT_RESET, CLIENT_STEP]:
                # Проверяем базовые события от клиента.
                if data == CLIENT_STARTED:
                    player.is_started = True
                elif data == CLIENT_RESET:
                    game.reset()
                # elif data == CLIENT_STEP:
                #     game.player_action(player.id, data)

                connect.send(player.json().encode('utf8'))

            if data == PLAYER_BUY_WORKER:
                print(f'{player.id} want buy a worker.')
                try:
                    player.buy_worker()
                except NotHaveMoney:
                    # TODO: Добавить клиенту оповещение о том, что у него недостаточно средств.
                    connect.send(player.json().encode('utf8'))
                else:
                    connect.send(player.json().encode('utf8'))

            if data == PLAYER_BUY_WARRIOR:
                print(f'{player.id} want buy a warrior')
                try:
                    player.buy_warrior()
                except NotHaveMoney:
                    connect.send(player.json().encode('utf8'))
                else:
                    connect.send(player.json().encode('utf8'))

            if data == PLAYER_ACTION_ATTACK:
                print(f'{player.id} want attack')
                pass

            if data == PLAYER_FINISH_STEP:
                print(f'{player.id} want step')
                pass

            if data == CLIENT_AWAIT:
                # Проверяем, что клиент ожидает участника для игры.
                check_game = game.check_start_game()
                if check_game:

                    connect.sendall(game.model.encoding())
                else:
                    connect.send(' '.encode('utf8'))

        except Exception as e:
            logging.exception(e)
            break

    print("Lost connection")
    game.remove_player(player)
    connect.close()


while True:
    connection, addr = s.accept()
    print("Connected to:", addr)

    player_id = game.delegate_gen_player_id()

    player = Player(id=player_id)
    game.add_player(player)
    start_new_thread(threaded_client, (connection, player))
