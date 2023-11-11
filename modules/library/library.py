from functools import lru_cache
from typing import Self, Type, NoReturn
from .._safe_connect import SafeConnect
from .products import *


__all__ = ('Library', )


# Переменные для аннотации
type Product = Album | Canvas | Journal | Layflat | Photobook | Photofolder | Subproduct


class Library:
    """Класс для работы с библиотекой продуктов"""
    __instance = None
    __s_con = SafeConnect('library.db')
    headers: dict[Type[Product], tuple[str, ...]] = {}

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            with cls.__s_con:
                cls.__update_product_headers()
        return cls.__instance

    def add(self, product: Product) -> None:
        """Метод добавления продукта в библиотеку"""
        with self.__s_con as con:
            self.__check_unique(product)
            req = ', '.join('?' * len(product))
            con.cursor.execute(f'INSERT INTO {product.category} {product._fields} VALUES ({req})', product)
            con.connect.commit()
            self.__update_product_headers()
        self.__get.cache_clear()

    def change(self, product: Product) -> None:
        """Внесение изменений в ячейку"""
        with self.__s_con as sc:
            req = ', '.join(f'{s}=?' for s in product._fields)
            sc.cursor.execute(f'UPDATE {product.category} SET {req} WHERE full_name=\'{product.full_name}\'', product)
            sc.connect.commit()
        self.__get.cache_clear()

    @classmethod
    def __check_unique(cls, product: Product) -> NoReturn | None:
        """Вспомогательная функция для библиотеки. Проверка на уникальность продукта"""
        cls.__s_con.cursor.execute(f'SELECT full_name FROM {product.category} WHERE full_name=?', (product.full_name, ))
        if cls.__s_con.cursor.fetchone(): raise Exception(f'{product.full_name}\nУже есть в библиотеке')

    def delete(self, category: str, full_name: str) -> None:
        """Удаление продукта из библиотеки."""
        with self.__s_con as sc:
            sc.cursor.execute(f'DELETE FROM {category} WHERE full_name=?', (full_name, ))
            sc.connect.commit()
            self.__update_product_headers()
        self.__get.cache_clear()

    @lru_cache
    def __get(self, category: Type[Product], name: str) -> Product: # type: ignore
        """Метод для получения объекта продукта по передоваемому имени. Возрващает объект или None."""
        with self.__s_con as sc:
            sc.cursor.execute(f'SELECT * FROM {category.__name__} WHERE full_name=?', (name, ))
            return category(*sc.cursor.fetchone()[1:])
    
    def get_ptype(self, category: str) -> Type[Product]:
        """Функция для получения пустого бланка для продукта"""
        return eval(category)

    def get(self, name: str) -> Product | None:
        """Возвращает объект продукта с которым связан тираж, если этот продукт есть в библиотеке"""
        for category, products in self.headers.items():
            for product in products:
                if name.endswith(product): return self.__get(category, product)

    @classmethod
    def __update_product_headers(cls) -> None:
        """Обновляет словрь имен продуктов в виде {имя продукта: категория}. Использовать только внутри менеджера"""
        for category in (Album, Canvas, Journal, Layflat, Photobook, Photofolder, Subproduct):
            cls.__s_con.cursor.execute(f'SELECT full_name FROM {category.__name__}')
            cls.headers[category] = tuple(n[0] for n in cls.__s_con.cursor.fetchall())
