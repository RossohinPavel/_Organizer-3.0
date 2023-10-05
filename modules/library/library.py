from functools import lru_cache
import modules.library.products as products
from modules.app_manager import AppManagerW
from modules.db_contextmanager import SafeConnect

__all__ = ('Library', )


class Library(AppManagerW):
    """Класс для работы с библиотекой продуктов"""
    _alias = 'lib'
    __s_con = SafeConnect('library.db')
    categories = tuple(getattr(products, x) for x in products.__all__)

    @classmethod
    def get_product_headers(cls) -> dict:
        """Возвращает словрь имен продуктов в виде {имя продукта: категория}"""
        dct = {}
        with cls.__s_con:
            for category in (x.__name__ for x in cls.categories):
                cls.__s_con.cursor.execute(f"SELECT full_name FROM {category}")
                dct.update((name[0], category) for name in cls.__s_con.cursor.fetchall())
        return dct

    @classmethod
    def get_blank(cls, category: str) -> object:
        """Возвращает объект продукта, который наполнен значениями по умолчанию"""
        return getattr(products, category)(True)

    def __init__(self):
        self.headers = self.get_product_headers()

    def add(self, prod_obj):
        """Метод добавления продукта в библиотеку
        :param prod_obj: Объект Продукта"""
        with self.__s_con:
            keys = ', '.join(f'{x}' for x in prod_obj.__dict__.keys())
            values = ', '.join(f'\'{x}\'' if type(x) == str else f'{x}' for x in prod_obj.__dict__.values())
            self.__s_con.cursor.execute(f'INSERT INTO {prod_obj.__class__.__name__} ({keys}) VALUES ({values})')
            self.__s_con.connect.commit()
        self.get.cache_clear()
        self.headers = self.get_product_headers()
    
    def change(self, prod_obj):
        """Внесение изменений в ячейку
        :param prod_obj: Объект Продукта"""
        with self.__s_con:
            sql_req = ', '.join(f'{k} = \"{v}\"' if type(v) == str else f'{k} = {v}' for k, v in prod_obj.__dict__.items())
            self.__s_con.cursor.execute(f'UPDATE {prod_obj.__class__.__name__} SET {sql_req} WHERE full_name=\'{prod_obj.full_name}\'')
            self.__s_con.connect.commit()
        self.get.cache_clear()
        self.headers = self.get_product_headers()
    
    def check_unique(self, prod_obj) -> bool:
        """Вспомогательная функция для библиотеки. Проверка на уникальность продукта"""
        with self.__s_con:
            self.__s_con.cursor.execute(f'SELECT * FROM {prod_obj.__class__.__name__} WHERE full_name=\'{prod_obj.full_name}\'')
            return not self.__s_con.cursor.fetchone()
    
    def delete(self, category: str, full_name: str):
        """Удаление продукта из библиотеки.
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        """
        with self.__s_con:
            self.__s_con.cursor.execute(f'DELETE FROM {category} WHERE full_name=\'{full_name}\'')
            self.__s_con.connect.commit()
        self.get.cache_clear()
        self.headers = self.get_product_headers()
    
    @lru_cache
    def get(self, name: str) -> object:
        """Метод для получения объекта продукта по передоваемому имени. Возрващает объект или None."""
        with self.__s_con:
            for category in (x.__name__ for x in self.categories):
                self.__s_con.cursor.execute(f'SELECT * FROM {category} WHERE full_name="{name}"')
                res = self.__s_con.cursor.fetchone()
                if res:
                    obj = getattr(products, category)()
                    self.__s_con.cursor.execute(f'PRAGMA table_info("{category}")')
                    table_name = self.__s_con.cursor.fetchall()
                    for i in range(1, len(res)):
                        obj.__dict__[table_name[i][1]] = res[i]
                    return obj

    def get_product_obj_from_name(self, name: str) -> object | None:
        """Возвращает объект продукта с которым связан тираж, если этот продукт есть в библиотеке"""
        for product_name in self.headers:
            if name.endswith(product_name):
                return self.get(product_name)