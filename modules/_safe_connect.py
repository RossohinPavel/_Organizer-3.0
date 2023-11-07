import sqlite3
from threading import Lock


class SafeConnect:
    """Менеджер контекста для безопасного подключения к базам данных sqlite3"""
    __slots__ = '__db_name', '__lock', 'connect', 'cursor'

    def __init__(self, db_name: str):
        self.__db_name = db_name
        self.__lock = Lock()
        self.connect = self.cursor = None

    def __enter__(self):
        """При входе в менеджер создаем подключение к бд и получаем её курсор. Блокируем сторонний доступ"""
        self.__lock.acquire()
        self.connect = sqlite3.connect(f'data/{self.__db_name}')
        self.cursor = self.connect.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """При выходе из менеджера, закрываем подключение и снимаем блок доступа."""
        self.__lock.release()
        self.cursor = None
        self.connect.close()
        return False
