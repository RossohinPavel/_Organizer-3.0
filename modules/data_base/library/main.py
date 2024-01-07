# Импорты для работы библиотеки
from ..data_base import DataBase
from .product import Product
from .properties import Properties

# Кэш
from functools import lru_cache

# Типизация
from typing import Type


class Library(DataBase):
    """Класс для работы с библиотекой продуктов"""
    data_base = 'library.db'

    Product = Product
    Properties = Properties

    @DataBase.safe_connect
    def get_headers(self) -> dict[Type[Product], list[tuple[int, str]]]:
        """
            Получение словаря из заголовков продуктов.
            Ключи - Типы продуктов
            Значения - Список из кортежей продуктов, 
            где перечисленны их id и name атрибуты
        """
        dct = {}
        for category in self.categories:
            self.cursor.execute(f'SELECT id, name FROM {category.__name__}')
            dct[category] = self.cursor.fetchall()
        return dct
    
    @DataBase.safe_connect
    def from_id(self, category: Type[Product], id: int) -> Product:
        """Получения объекта продукта по передоваемому id."""
        self.cursor.execute(f'SELECT * FROM {category.__name__} WHERE id=?', (id, ))
        return category(*self.cursor.fetchone()[1:])    #type: ignore
    
    @DataBase.safe_connect
    def get_aliases(self, category: Type[Product], id: int) -> list:
        """Получение списка псевдонимов продукта"""
        self.cursor.execute(f"""
            SELECT alias 
            FROM Aliases 
            WHERE category=? AND product_id=?
            """, 
            (category.__name__, id)
        )
        return self.cursor.fetchall()

    @DataBase.safe_connect
    def add(self, product: Product) -> None:
        """Добавление продукта в библиотеку"""
        # Проверка на уникальность продукта
        self.__check_unique_name(product)

        # Составление запроса sql и обновление бд
        req = ', '.join('?' * len(product))
        self.cursor.execute(f'INSERT INTO {product.category} {product._fields} VALUES ({req})', product)
        self.connect.commit()
        self.get.cache_clear()
    
    @DataBase.safe_connect
    def change(self, id: int, product: Product, aliases: tuple[str]) -> None:
        """Внесение изменений в продукт"""
        # Проверка на уникальность продукта
        self.__check_unique_name(product, id)

        # Составление запроса sql и обновление бд продукта
        req = ', '.join(f'{f}=?' for f in product._fields)
        self.cursor.execute(f'UPDATE {product.category} SET {req} WHERE id={id}', product)

        # Обновление псевдониов для продукции
        self.__update_aliases(id, product, aliases)

        self.connect.commit()
        self.get.cache_clear()
    
    def __update_aliases(self, id: int, product: Product, aliases: tuple[str]) -> None:
        """Обновление псевдонимов для продукта."""
        # Получаем множество псевдонимов из базы данных
        self.cursor.execute(
            """SELECT alias FROM Aliases WHERE category=? AND product_id=?""",
            (product.category, id)
        )
        res = set(x[0] for x in self.cursor.fetchall())

        # Рассчитываем псевдонимы для удаления и для добавления
        aliases = set(aliases)                          #type: ignore
        to_del, to_add = res - aliases, aliases - res   #type: ignore
        try:
            if to_del:
                req = ', '.join(repr(x) for x in to_del)
                self.cursor.execute(
                    f"""DELETE FROM Aliases WHERE alias IN ({req}) AND category=? AND product_id=?""",
                    (product.category, id)
                )
            
            if to_add:
                self.cursor.executemany(
                    'INSERT INTO Aliases (alias, category, product_id) VALUES (?, ?, ?)', 
                    ((x, product.category, id) for x in to_add)
                )
        except Exception as e:
            raise Exception(f'Добавляемые псевдонимы не уникальны\n{e}')

    def __check_unique_name(self, product: Product, id: int = 0) -> None:
        """
            Проверка имени продукта на уникальность. 
            Проверка происходит по всем таблицам
        """
        self.cursor.execute("""
        SELECT EXISTS (
            SELECT id, name FROM(
                SELECT id, name FROM Album
                UNION SELECT id, name FROM Canvas
                UNION SELECT id, name FROM Journal
                UNION SELECT id, name FROM Layflat
                UNION SELECT id, name FROM Photobook
                UNION SELECT id, name FROM Photofolder
                UNION SELECT id, name FROM Subproduct
            )
            WHERE id != ? AND name=?
        )""",
        (id, product.name)
        )
        if self.cursor.fetchone()[0]:
            raise Exception(f'{product.name}\nУже есть в библиотеке')

    @DataBase.safe_connect
    def delete(self, category: Type[Product], id: int) -> None:
        """Удаление продукта из библиотеки."""
        # Удаление продукта из библиотеки
        self.cursor.execute(f'DELETE FROM {category.__name__} WHERE id=?', (id, ))
        # Очитска таблицы псевдонимов от удаляемого продукта
        self.cursor.execute(f'DELETE FROM Aliases WHERE product_id=?', (id, ))
        self.connect.commit()
        self.get.cache_clear()

    @lru_cache
    @DataBase.safe_connect
    def get(self, name: str) -> Product | None: 
        """
            Возвращает объект продукта с которым связан тираж, 
            если этот продукт есть в библиотеке.
        """
        _, name = name.rsplit('-', maxsplit=1)
        self.cursor.execute('SELECT category, product_id FROM Aliases WHERE alias=?', (name, ))
        res = self.cursor.fetchone()

        if res:
            category, id = res
            self.cursor.execute(f'SELECT * FROM {category} WHERE id=?', (id, ))
            return eval(f'{category}(*self.cursor.fetchone()[1:])')
