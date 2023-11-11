from sqlite3 import connect, Connection, Cursor
from threading import Lock
from typing import Self


class SafeConnect:
    """Менеджер контекста для безопасного подключения к базам данных sqlite3"""
    __slots__ = '__db_name', '__lock', 'connect', 'cursor'

    def __init__(self, db_name: str):
        self.__db_name = db_name
        self.__lock = Lock()
        self.connect: Connection
        self.cursor: Cursor

    def __enter__(self) -> Self:
        """При входе в менеджер создаем подключение к бд и получаем её курсор. Блокируем сторонний доступ"""
        self.__lock.acquire()
        self.connect = connect(f'data/{self.__db_name}')
        self.cursor = self.connect.cursor()
        return self

    def __exit__(self, *args) -> bool:
        """При выходе из менеджера, закрываем подключение и снимаем блок доступа."""
        self.__lock.release()
        self.connect.close()
        return False
