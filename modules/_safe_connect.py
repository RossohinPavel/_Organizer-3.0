import sqlite3
from threading import Lock


class SafeConnect:
    """Менеджер контекста для безопасного подключения к базам данных sqlite3"""
    __slots__ = '__db_name', 'connect', 'cursor'

    def __new__(cls, db_name: str):
        if not getattr(cls, f'__{db_name}l', None):
            setattr(cls, f'__{db_name}l', Lock())
        obj = super().__new__(cls)
        obj.__db_name = db_name
        obj.connect = obj.cursor = None
        return obj

    def __enter__(self):
        """При входе в менеджер создаем подключение к бд и получаем ее курсор. Блокируем сторонний доступ"""
        getattr(self, f'__{self.__db_name}l').acquire()
        self.connect = sqlite3.connect(f'data/{self.__db_name}')
        self.cursor = self.connect.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """При выходе из менеджера, закрываем подключение и снимаем блок с доступа."""
        getattr(self, f'__{self.__db_name}l').release()
        self.cursor = None
        self.connect.close()
        return False
