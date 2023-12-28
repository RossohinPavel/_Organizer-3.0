from functools import lru_cache
from ...mytyping import Type, NoReturn, Categories
from ..data_base import DataBase
from .products import *
from .properties import Properties


class Library(DataBase):
    """Класс для работы с библиотекой продуктов"""
    data_base = 'library.db'

    products = (Album, Canvas, Journal, Layflat, Photobook, Photofolder, Subproduct)
    properties = Properties

    @DataBase.safe_connect
    def get_headers(self) -> dict[Type[Categories], list[tuple[int, str]]]:
        """
            Получение словаря из заголовков продуктов.
            Ключи - Типы продуктов
            Значения - Список из кортежей продуктов, 
            где перечисленны их id и name атрибуты
        """
        dct = {}
        for product in self.products:
            self.cursor.execute(f'SELECT id, name FROM {product.__name__}')
            dct[product] = self.cursor.fetchall()
        return dct
    
    @DataBase.safe_connect
    def from_id(self, category: str | Type[Categories], id: int) -> Categories:
        """Получения объекта продукта по передоваемому id."""
        if isinstance(category, str):
            category = eval(category)
        self.cursor.execute(f'SELECT * FROM {category.__name__} WHERE id=?', (id, ))
        return category(*self.cursor.fetchone()[1:])    #type: ignore


    # @DataBase.safe_connect
    # def add(self, product: Product) -> None:
    #     """Метод добавления продукта в библиотеку"""
    #     self.__check_unique(product)
    #     req = ', '.join('?' * len(product))
    #     self.cursor.execute(f'INSERT INTO {product.category} {product._fields} VALUES ({req})', product)
    #     self.connect.commit()
    #     self.__update_product_headers()
    #     self.get.cache_clear()

    # @DataBase.safe_connect
    # def change(self, product: Product) -> None:
    #     """Внесение изменений в ячейку"""
    #     req = ', '.join(f'{s}=?' for s in product._fields)
    #     self.cursor.execute(f'UPDATE {product.category} SET {req} WHERE full_name=\'{product.full_name}\'', product)
    #     self.connect.commit()
    #     self.get.cache_clear()

    # def __check_unique(self, product: Product) -> NoReturn | None:
    #     """Вспомогательная функция для библиотеки. Проверка на уникальность продукта"""
    #     for name in (y for x in self.headers.values() for y in x):
    #         if name == product.full_name:
    #             raise Exception(f'{product.full_name}\nУже есть в библиотеке')

    # @DataBase.safe_connect
    # def delete(self, category: str, full_name: str) -> None:
    #     """Удаление продукта из библиотеки."""
    #     self.cursor.execute(f'DELETE FROM {category} WHERE full_name=?', (full_name, ))
    #     self.connect.commit()
    #     self.__update_product_headers()
    #     self.get.cache_clear()

    # @DataBase.safe_connect    
    # def __get(self, category: Type[Product], name: str) -> Product: # type: ignore
    #     """Метод для получения объекта продукта по передоваемому имени. Возрващает объект или None."""
    #     self.cursor.execute(f'SELECT * FROM {category.__name__} WHERE full_name=?', (name, ))
    #     return category(*self.cursor.fetchone()[1:])

    # @lru_cache
    # def get(self, name: str) -> Product:    # type: ignore
    #     """Возвращает объект продукта с которым связан тираж, если этот продукт есть в библиотеке"""
    #     for category, products in self.headers.items():
    #         for product in products:
    #             if name.endswith(product): 
    #                 return self.__get(category, product)

    # def __update_product_headers(self) -> None:
    #     """
    #         Обновляет словрь имен продуктов в виде {имя продукта: категория}. 
    #         Использовать только внутри менеджера
    #     """
    #     for category in (Album, Canvas, Journal, Layflat, Photobook, Photofolder, Subproduct):
    #         self.cursor.execute(f'SELECT full_name FROM {category.__name__}')
    #         self.headers[category] = tuple(n[0] for n in self.cursor.fetchall())
