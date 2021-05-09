import socket
import pickle
from typing import Optional
from pickle import PicklingError
from constants import PORT, HOST


class HasNotSocketConnection(Exception):
    """Ошибка, что нет соединение с сокетом, на случай, если произошел обрыв связи.
    """
    pass


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (HOST, PORT)
        self.has_connect: bool = False

        # Инициализировали нужные данные и соединяемся по сокету.
        self.connect()

    def get_pos(self) -> Optional[int]:
        if not self.has_connect:
            raise HasNotSocketConnection('Not socket connection.')

        try:
            return self.client.recv(2048).decode()
        except Exception as e:
            pass

        return None

    def connect(self):
        if not self.has_connect:
            # Предотвращаем повторного подключения, т.к. оно уже установлено
            # В случае, если код будет вызван дважды.
            self.client.connect(self.addr)
            self.has_connect = True

    def disconnect(self):
        self.client.close()
        self.has_connect = False

    def send(self, data: str):
        # TODO: Узнать и обработать статус.
        status: int = self.client.send(data.encode('utf-8'))

        try:
            return pickle.loads(self.client.recv(2048 * 2))
        except PicklingError as e:
            print(e)
        except Exception as e:
            print('Непредвиденная ошибка.')
