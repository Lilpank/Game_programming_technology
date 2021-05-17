import json
import socket
import logging
from _thread import *
from models.game.player import Player, NotHaveMoney
from controllers.game import GameController
from models.data.room import GameRoom
from itertools import chain
from models.data.game import Response
from constants import HOST, PORT, CLIENT_RESET, CLIENT_STARTED, CLIENT_STEP, CLIENT_AWAIT, PLAYER_BUY_WORKER, \
    PLAYER_BUY_WARRIOR, PLAYER_FINISH_STEP, PLAYER_ACTION_ATTACK
from models.data.game import CREATE_WORKER, CREATE_WARRIOR, CREATE_FINISH_STEP, CREATE_WAR_STEP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")

game = GameController()


def threaded_client(connect: socket.socket):
    player = None
    while True:
        try:
            data = connect.recv(4096).decode()
            if not data:
                break

            player_data = json.loads(data)
            data = player_data['data']
            player = game.model.players[player_data['id']]

            if data in [CLIENT_STARTED, CLIENT_RESET, CLIENT_STEP]:
                # Проверяем базовые события от клиента.
                if data == CLIENT_STARTED:
                    player.is_started = True

                elif data == CLIENT_RESET:
                    game.reset()

                elif data == CLIENT_STEP:
                    game.player_action(player.id, data)

                connect.send(Response(data_class=2, data=player).json().encode('utf-8'))

            if data == PLAYER_BUY_WORKER:
                print(f'{player.id} want buy a worker.')
                try:
                    game.player_action(player.id, CREATE_WORKER)
                except NotHaveMoney:
                    # TODO: Добавить клиенту оповещение о том, что у него недостаточно средств.
                    connect.send(Response(data_class=2, data=player).json().encode('utf8'))
                else:
                    connect.send(Response(data_class=2, data=player).json().encode('utf8'))

            if data == PLAYER_BUY_WARRIOR:
                print(f'{player.id} want buy a warrior')
                try:
                    game.player_action(player.id, CREATE_WARRIOR)
                except NotHaveMoney:
                    # TODO: Добавить клиенту оповещение о том, что у него недостаточно средств.
                    connect.send(Response(data_class=2, data=player).json().encode('utf8'))
                else:
                    connect.send(Response(data_class=2, data=player).json().encode('utf8'))

            if data == PLAYER_ACTION_ATTACK:
                print(f'{player.id} want attack')
                game.player_action(player.id, CREATE_WAR_STEP)
                connect.sendall(Response(data_class=2, data=player).json().encode('utf8'))

            if data == PLAYER_FINISH_STEP:
                print(f'{player.id} want finish step')
                game.player_action(player.id, CREATE_FINISH_STEP)
                connect.sendall(Response(data_class=2, data=player).json().encode('utf8'))

            if data == CLIENT_AWAIT:
                # Проверяем, что клиент ожидает участника для игры.
                check_game = game.check_start_game()

                if check_game:
                    players = game.chunk_active_players(
                        chain.from_iterable([
                            room.get_contains_players() for room in game.rooms
                        ])
                    )

                    try:
                        if players:
                            game_room = GameRoom()
                            game_room.set_players(players)
                            game.rooms.append(game_room)

                            for player in players:
                                player.is_started = False
                                player.is_gaming = True

                            connect.sendall(Response(data_class=1, data=game_room).json().encode('utf-8'))
                        else:
                            connect.sendall(' '.encode('utf8'))
                    except Exception as e:
                        logging.exception(e)
                        connect.sendall(' '.encode('utf8'))
                elif player.is_gaming:
                    for room in game.rooms:
                        if player.id in room.get_contains_players():
                            connect.sendall(Response(data_class=1, data=room).json().encode('utf-8'))
                else:
                    connect.send(' '.encode('utf8'))

        except Exception as e:
            logging.exception(e)
            break

    print("Lost connection")
    if player:
        game.remove_player(player)
    connect.close()


while True:
    connection, addr = s.accept()
    print("Connected to:", addr)

    player_id = game.delegate_gen_player_id()

    player = Player(id=player_id)

    game.add_player(player)
    connection.send(player.json().encode('utf8'))
    start_new_thread(threaded_client, (connection,))
