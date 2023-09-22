import sqlite3
from threading import Lock


class SafeConnect:
    """Менеджер контекста для безопасного подключения к базам данных sqlite3"""
    __slots__ = '__db_name', 'connect', 'cursor'
    __lock_dct = {}

    def __init__(self, db_name: str):
        self.__db_name = db_name
        self.connect = None
        self.cursor = None

    def __enter__(self):
        if self.__db_name not in self.__lock_dct:
            self.__lock_dct[self.__db_name] = Lock()
        self.__lock_dct[self.__db_name].acquire()
        self.connect = sqlite3.connect(f'data/{self.__db_name}')
        self.cursor = self.connect.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock_dct[self.__db_name].release()
        self.cursor = None
        self.connect.close()
        return False
