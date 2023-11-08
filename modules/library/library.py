from functools import lru_cache
from typing import Self

from .._safe_connect import SafeConnect
from .properties import Blank
from .products import *


__all__ = ('Library', )


class Library:
    """Класс для работы с библиотекой продуктов"""
    __instance = None
    __s_con = SafeConnect('library.db')
    headers = {}

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        with self.__s_con:
            self.__update_product_headers()

    def add(self, product: Product):
        """Метод добавления продукта в библиотеку
        :param product: Объект Продукта"""
        with self.__s_con as con:
            attrs = tuple(product)
            req = ', '.join('?' * len(attrs))
            con.cursor.execute(f'INSERT INTO {product.category} {attrs} VALUES ({req})', tuple(product.values()))
            con.connect.commit()
            self.__update_product_headers()
        self.get.cache_clear()

    def change(self, prod_obj: object):
        """Внесение изменений в ячейку
        :param prod_obj: Объект Продукта"""
        with self.__s_con as con:
            req = ', '.join(f'{s}=?' for s in prod_obj)
            val = tuple(prod_obj.values())
            con.cursor.execute(f'UPDATE {prod_obj.category} SET {req} WHERE full_name=\'{prod_obj.full_name}\'', val)
            con.connect.commit()
        self.get.cache_clear()

    def check_unique(self, product: Product) -> bool:
        """Вспомогательная функция для библиотеки. Проверка на уникальность продукта"""
        with self.__s_con as con:
            con.cursor.execute(f'SELECT full_name FROM {product.category} WHERE full_name=?', (product.full_name, ))
            return not self.__s_con.cursor.fetchone()

    def delete(self, category: str, full_name: str):
        """Удаление продукта из библиотеки.
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        """
        with self.__s_con:
            self.__s_con.cursor.execute(f'DELETE FROM {category} WHERE full_name=?', (full_name, ))
            self.__s_con.connect.commit()
            self.__update_product_headers()
        self.get.cache_clear()

    @lru_cache
    def get(self, category: Product, name: str) -> object:
        """Метод для получения объекта продукта по передоваемому имени. Возрващает объект или None."""
        with self.__s_con as con:
            con.cursor.execute(f'SELECT * FROM {category.__name__} WHERE full_name=?', (name, ))
            res = con.cursor.fetchone()
            obj = category()
            for i, attr in enumerate(obj, 1):
                setattr(obj, attr, res[i])
            return obj

    @classmethod
    def get_blank(cls, category_name: str) -> object:
        """Возвращает объект продукта, который наполнен значениями по умолчанию"""
        for category in cls.headers:
            if category.__name__ == category_name:
                return Blank(category).create_blank()

    def get_product_obj_from_name(self, name: str) -> object | None:
        """Возвращает объект продукта с которым связан тираж, если этот продукт есть в библиотеке"""
        for category, products in self.headers.items():
            for product in products:
                if name.endswith(product):
                    return self.get(category, product)

    @classmethod
    def __update_product_headers(cls):
        """Обновляет словрь имен продуктов в виде {имя продукта: категория}. Использовать только внутри менеджера"""
        for category in (Album, Canvas, Journal, Layflat, Photobook, Photofolder, Subproduct):
            cls.__s_con.cursor.execute(f'SELECT full_name FROM {category.__name__}')
            cls.headers[category] = tuple(n[0] for n in cls.__s_con.cursor.fetchall())
