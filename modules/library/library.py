import sqlite3
from functools import lru_cache
from modules.library.products import *
from modules.app_manager import AppManagerW


__all__ = ('Library', )


class Library(AppManagerW):
    __db = 'data/library.db'
    __timeout = 10
    __categories = ('Album', 'Canvas', 'Journal', 'Layflat', 'Photobook', 'Photofolder',  'Subproduct')

    @staticmethod
    def __safe_connect(do_commit=False):
        """Декоратор для безопасного подключения к БД"""
        def decorator(func):
            def wrapper(instance, *args, **kwargs):
                with sqlite3.connect(Library.__db, timeout=Library.__timeout) as connect:
                    cursor = connect.cursor()
                    res = func(instance, cursor, *args, **kwargs)
                    if do_commit:
                        connect.commit()
                    return res
            wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
            return wrapper
        return decorator

    @__safe_connect(do_commit=True)
    def add(self, cursor, prod_obj):
        """Метод добавления продукта в библиотеку
        :param cursor: Сылка на объект cursor базы данных
        :param prod_obj: Объект Продукта
        """
        keys = ', '.join(f'{x}' for x in prod_obj.__dict__.keys())
        values = ', '.join(f'\'{x}\'' if type(x) == str else f'{x}' for x in prod_obj.__dict__.values())
        cursor.execute(f'INSERT INTO {prod_obj.category} ({keys}) VALUES ({values})')
        self.get.cache_clear()

    @__safe_connect(do_commit=True)
    def change(self, cursor, prod_obj):
        """Внесение изменений в ячейку
        :param cursor: Cылка на объект cursor базы данных
        :param prod_obj: Объект Продукта
        """
        sql_req = ', '.join(f'{k} = \"{v}\"' if type(v) == str else f'{k} = {v}' for k, v in prod_obj.__dict__.items())
        cursor.execute(f'UPDATE {prod_obj.category} SET {sql_req} WHERE full_name=\'{prod_obj.full_name}\'')
        self.get.cache_clear()

    @__safe_connect()
    def check_unique(self, cursor, prod_obj) -> bool:
        """Вспомогательная функция для библиотеки. Проверка на уникальность продукта"""
        cursor.execute(f'SELECT * FROM {prod_obj.category} WHERE full_name=\'{prod_obj.full_name}\'')
        return not cursor.fetchone()

    @__safe_connect(do_commit=True)
    def delete(self, cursor, category: str, full_name: str):
        """Удаление продукта из библиотеки.
        :param cursor: Ссылка на объект cursor базы данных. Передавать не надо. Его подставит декортаор.
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        """
        cursor.execute(f'DELETE FROM {category} WHERE full_name=\'{full_name}\'')
        self.get.cache_clear()
        print(self.get.cache_info())

    @lru_cache
    @__safe_connect()
    def get(self, cursor, name: str):
        """Метод для получения объекта продукта по передоваемому имени. Возрващает объект или None."""
        for category in self.__categories:
            cursor.execute(f'SELECT * FROM {category} WHERE full_name="{name}"')
            res = cursor.fetchone()
            if res:
                obj = eval(f'{category}()')
                cursor.execute(f'PRAGMA table_info("{category}")')
                table_name = cursor.fetchall()
                for i in range(1, len(res)):
                    obj.__dict__[table_name[i][1]] = res[i]
                return obj

    @__safe_connect()
    def get_product_headers(self, cursor) -> dict:
        """Возвращает словрь имен продуктов в виде {Категория=Русское имя категории: (продукт1, продукт2, ...)}"""
        dct = {}
        for category in self.__categories:
            cursor.execute(f"SELECT full_name FROM {category}")
            dct[f'{category}=' + eval(f'{category}.rus_name')] = tuple(x[0] for x in cursor.fetchall())
        return dct

    @staticmethod
    def get_blank(category: str) -> object:
        """Возвращает объект продукта, который наполнен значениями по умолчанию"""
        return eval(f'{category}(True)')
