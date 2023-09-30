from functools import lru_cache
import modules.library.products as products
from modules.app_manager import AppManagerW
from modules.db_contextmanager import SafeConnect

__all__ = ('Library', )


class Library(AppManagerW):
    """Класс для работы с библиотекой продуктов"""
    __s_con = SafeConnect('library.db')
    _alias = 'lib'
    categories = tuple(getattr(products, x) for x in products.__all__)

    @classmethod
    def get_product_headers(cls) -> dict:
        """Возвращает словрь имен продуктов в виде {имя продукта: категория}"""
        dct = {}
        with cls.__s_con:
            for category in cls.categories:
                cls.__s_con.cursor.execute(f"SELECT full_name FROM {category.__name__}")
                for name in cls.__s_con.cursor.fetchall():
                    dct[name[0]] = category.__name__
            return dct

    @staticmethod
    def get_blank(category: str) -> object:
        """Возвращает объект продукта, который наполнен значениями по умолчанию"""
        return getattr(products, category)(True)

    def __init__(self):
        self.headers = self.get_product_headers()

    # def add(self, prod_obj):
    #     """Метод добавления продукта в библиотеку
    #     :param prod_obj: Объект Продукта"""
    #     with self.__s_con:
    #         keys = ', '.join(f'{x}' for x in prod_obj.__dict__.keys())
    #         values = ', '.join(f'\'{x}\'' if type(x) == str else f'{x}' for x in prod_obj.__dict__.values())
    #         self.__s_con.cursor.execute(f'INSERT INTO {prod_obj.category} ({keys}) VALUES ({values})')
    #         self.__s_con.connect.commit()
    #     self.get.cache_clear()
    #
    # def change(self, prod_obj):
    #     """Внесение изменений в ячейку
    #     :param prod_obj: Объект Продукта"""
    #     with self.__s_con:
    #         sql_req = ', '.join(f'{k} = \"{v}\"' if type(v) == str else f'{k} = {v}' for k, v in prod_obj.__dict__.items())
    #         self.__s_con.cursor.execute(f'UPDATE {prod_obj.category} SET {sql_req} WHERE full_name=\'{prod_obj.full_name}\'')
    #         self.__s_con.connect.commit()
    #     self.get.cache_clear()
    #
    # def check_unique(self, prod_obj) -> bool:
    #     """Вспомогательная функция для библиотеки. Проверка на уникальность продукта"""
    #     with self.__s_con:
    #         self.__s_con.cursor.execute(f'SELECT * FROM {prod_obj.category} WHERE full_name=\'{prod_obj.full_name}\'')
    #         return not self.__s_con.cursor.fetchone()
    #
    # def delete(self, category: str, full_name: str):
    #     """Удаление продукта из библиотеки.
    #     :param category: Категория продукта / название таблицы
    #     :param full_name: Имя продукта
    #     """
    #     with self.__s_con:
    #         self.__s_con.cursor.execute(f'DELETE FROM {category} WHERE full_name=\'{full_name}\'')
    #         self.__s_con.connect.commit()
    #     self.get.cache_clear()
    #
    # @lru_cache
    # def get(self, name: str):
    #     """Метод для получения объекта продукта по передоваемому имени. Возрващает объект или None."""
    #     with self.__s_con:
    #         for category in self.__categories:
    #             self.__s_con.cursor.execute(f'SELECT * FROM * WHERE full_name="{name}"')
    #             res = self.__s_con.cursor.fetchone()
    #             if res:
    #                 obj = eval(f'{category}()')
    #                 self.__s_con.cursor.execute(f'PRAGMA table_info("{category}")')
    #                 table_name = self.__s_con.cursor.fetchall()
    #                 for i in range(1, len(res)):
    #                     obj.__dict__[table_name[i][1]] = res[i]
    #                 return obj
