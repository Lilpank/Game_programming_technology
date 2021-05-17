import socket
from pydantic import ValidationError
from typing import Optional, Any
from constants import PORT, HOST, CLIENT_AWAIT
from models.data.game import GameModel
from models.game.player import Player
from models.data.room import GameRoom
import json


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
        if data.decode('utf-8') == ' ':
            return None

        try:
            prepare_data = json.loads(data)
        except json.JSONDecodeError as e:
            print(e)
            return None
        print(prepare_data)
        if prepare_data['data_class'] == 2:
            model = Player(**prepare_data['data'])
        elif prepare_data['data_class'] == 1:
            model = GameRoom(**prepare_data['data'])
        else:
            model = None
        return model
