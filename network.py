import socket
from pydantic import ValidationError
from typing import Optional, Any
from constants import PORT, HOST, CLIENT_AWAIT
from models.data.game import GameModel
from models.game.player import Player


class HasNotSocketConnection(Exception):
    """Ошибка, что нет соединение с сокетом, на случай, если произошел обрыв связи.
    """
    pass


class Network:
    """Класс, отвечающий за соединение клиента с сервером.
    """

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (HOST, PORT)
        self.has_connect: bool = False

        # Инициализировали нужные данные и соединяемся по сокету.
        self.connect()

    def get_pos(self) -> Optional[int]:
        if not self.has_connect:
            raise HasNotSocketConnection('Not socket connection.')

        try:
            return self.connection.recv(2048).decode()
        except Exception as e:
            pass

        return None

    def connect(self):
        if not self.has_connect:
            # Предотвращаем повторного подключения, т.к. оно уже установлено
            # В случае, если код будет вызван дважды.
            self.connection.connect(self.addr)
            self.has_connect = True

    def disconnect(self):
        self.connection.close()
        self.has_connect = False

    def send_and_get(self, data: str) -> Any:
        status: int = self.connection.send(data.encode('utf-8'))
        data = self.connection.recv(2048 * 2)

        if data.decode('utf8') == ' ':
            return None

        model = None
        try:
            model = GameModel.parse_raw(data)
        except ValidationError:
            model = Player.parse_raw(data)
        except Exception as e:
            print(e)
            print('Непредвиденная ошибка.')

        return model
