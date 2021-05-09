import socket
from _thread import *
import pickle
from game import Game
from constants import HOST, PORT
import _json

"""
Для сетевого взаимодействия через JSON используешь обычную библиотеку json.
Для правильной архитектуры, чтобы не запутаться в объектах используешь https://pydantic-docs.helpmanual.io/
Через Pydantic описываешь классом свои объекты (дата классы), это просто классы, которые будут содержать данные
из строки json и автоматом конвертироваться в объекты. на youtub'e просмотри Диджитализируй - pydantic. 
Коротко и понятно расскажет. А Pickle удаляй.
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if data is not None:
                if gameId in games:
                    game = games[gameId]

                    if not data:
                        break
                    else:
                        if data == "reset":
                            game.reset_went()
                        elif data != "get":
                            game.play(p, data)

                        conn.sendall(pickle.dumps(game))
                else:
                    break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
