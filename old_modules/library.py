import sqlite3
from functools import lru_cache
import threading as th


class Library:
    """
    Класс для работы с базой данных библиотеки продуктов.
    """
    __instance = None
    __db = '../data/library.db'
    __timeout = 10

    # @staticmethod
    # def __safe_connect(func):
    #     """Декоратор для безопасного подключения к БД"""
    #     def wrapper(instance, *args, **kwargs):
    #         with sqlite3.connect(Library.__db, timeout=Library.__timeout) as connect:
    #             cursor = connect.cursor()
    #             return func(instance, cursor, *args, **kwargs)
    #
    #     wrapper.__name__ = func.__name__
    #     wrapper.__doc__ = func.__doc__
    #     return wrapper
    #
    # @lru_cache
    # @__safe_connect
    # def get_product_values(self, cursor, category: str, full_name: str) -> dict:
    #     """
    #     Метод для получения данных из бд в виде словаря
    #     :param cursor: Объект курсора, который передается декоратором
    #     :param category: Категория продукта / название таблицы
    #     :param full_name: Имя продукта
    #     """
    #     if self._cache_clear:
    #         print('Очистка кэша')
    #         self.get_product_values.cache_clear()
    #     print('сработал метод')
    #     keys = tuple(self.blank(category))
    #     sql_req = ', '.join(f'\"{x}\"' for x in keys)
    #     cursor.execute(f'SELECT {sql_req} FROM {category} WHERE full_name=\'{full_name}\'')
    #     values = cursor.fetchone()
    #     return {keys[i]: values[i] for i in range(len(keys))}


# if __name__ == '__main__':
#     obj = Library()
#     test_func = lambda x: print(id(x))
#     t1 = th.Thread(target=test_func, args=(obj, ))
#     t2 = th.Thread(target=test_func, args=(obj, ))
#     t1.start()
#     t2.start()