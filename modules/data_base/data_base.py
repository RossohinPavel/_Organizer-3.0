from sqlite3 import connect, Connection, Cursor
from threading import Lock
from typing import Self


class DataBase:
    """Реализует общую логику работы с базами данных sqlite3"""
    __slots__ = '_lock', 'connect', 'cursor'

    # Имя базы данных, к которой будет совершено подключение
    data_base: str = 'None'

    def __init__(self):
        self._lock = Lock()
        self.connect: Connection
        self.cursor: Cursor

    @staticmethod
    def safe_connect(func):
        """Декоратор для безопасного подключения к бд"""

        def wrapper(self, *args, **kwargs):
            print(self, func)
            with self._lock:
                self.connect = connect(f'data/{self.data_base}')
                self.cursor = self.connect.cursor()
                res = func(self, *args, **kwargs)
                self.connect.close()
                return res

        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper
