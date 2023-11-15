from typing import NamedTuple
from ._safe_connect import SafeConnect


class Photo(NamedTuple):
    """Инофрмация о фотопечати."""
    name: str                               # Имя тиража
    count: int                              # Счетчик отпечатков


class Edition(NamedTuple):
    """Информация о тираже."""
    name: str                               # Имя тиража
    covers: int                             # Счетчик обложек
    pages: int | None                       # Счетчик разворотов
    ccount: str | None                      # Комплексный счетчик обложек/разворотов
    comp: str | None                        # Тип совмещения тиража (актуально для книг)


class Order(NamedTuple):
    """Информация о заказе."""
    name: str                               # Имя заказа, он же его номер
    creation_date: str                      # Дата загрузки заказа на сервер
    customer_name: str                      # Имя заказчика
    customer_address: str                   # Адрес заказчика
    price: float                            # Общая сумма заказа
    photo: tuple[Photo, ...] | None         # Кортеж объектов фотопечати заказа
    content: tuple[Edition, ...] | None     # Кортеж объектов тиражей заказа


class Log:
    """Класс предостовляющий доступ к чтению и записи лога заказов"""
    __slots__ = '__s_con'

    def __init__(self) -> None:
        self.__s_con = SafeConnect('log.db')

    # def update_records(self, lst: list):
    #     """Сборная ф-я для обновления библиотеки"""
    #     lst.reverse()
    #     with self.__s_con:
    #         self.__update_orders_table(lst)
    #         self.__s_con.connect.commit()

    # def __update_orders_table(self, lst):
    #     """Обновление данных в основной таблице информации о заказе"""
    #     for order_dc in lst:
    #         keys, values = zip(*((k, v) for k, v in order_dc.__dict__.items() if k not in ('photo', 'content')))
    #         self.__s_con.cursor.execute(f'SELECT EXISTS (SELECT name FROM Orders WHERE name={order_dc.name} LIMIT 1)')
    #         if self.__s_con.cursor.fetchone()[0]:
    #             req = ', '.join(f'{keys[x]} = \'{values[x]}\'' for x in range(2, 5))
    #             self.__s_con.cursor.execute(f'UPDATE Orders SET {req} WHERE name={values[0]}')
    #         else:
    #             self.__s_con.cursor.execute(f'INSERT INTO Orders {keys} VALUES {values}')
    #         self.__update_editions_tables(*order_dc.content, *order_dc.photo)

    # def __update_editions_tables(self, *edt_tuple):
    #     """Обновление данных в таблице тиражей"""
    #     for edt in edt_tuple:
    #         table = 'Editions' if edt.__class__.__name__ == 'Edition' else 'Photos'
    #         keys, values = zip(*((k, v) for k, v in edt.__dict__.items() if v is not None))
    #         self.__s_con.cursor.execute(f'SELECT EXISTS(SELECT name FROM {table} WHERE order_name={values[0]} AND name=\'{values[1]}\' LIMIT 1)')
    #         if self.__s_con.cursor.fetchone()[0]:
    #             req = ', '.join(f'{keys[x]} = \'{values[x]}\'' for x in range(2, len(keys)))
    #             self.__s_con.cursor.execute(f'UPDATE {table} SET {req} WHERE order_name={values[0]} AND name=\'{values[1]}\'')
    #         else:
    #             self.__s_con.cursor.execute(f'INSERT INTO {table} {keys} VALUES {values}')

    def get(self, order_name: str) -> Order | None:
        """Получение объекта заказа из лога."""
        with self.__s_con:
            self.__s_con.cursor.execute('SELECT * FROM Orders WHERE name=?', (order_name, ))
            res = self.__s_con.cursor.fetchone()
            if res: return Order(*res[1:], self.__get_photos(order_name), self.__get_editions(order_name))  #type: ignore
    
    def __get_photos(self, order_name: str) -> tuple[Photo, ...] | None:
        """Вспомогательная ф-я для получения информации о фотопечати в заказе"""
        self.__s_con.cursor.execute('SELECT name, count FROM Photos WHERE order_name=?', (order_name, ))
        res = self.__s_con.cursor.fetchall()
        if res: return tuple(Photo(*r) for r in res)

    def __get_editions(self, order_name: str) -> tuple[Edition, ...] | None:
        """Вспомогательная ф-я для получения информации о тиражах в заказе"""
        self.__s_con.cursor.execute('SELECT name, covers, pages, ccount, comp FROM Editions WHERE order_name=?', (order_name, ))
        res = self.__s_con.cursor.fetchall()
        if res: return tuple(Edition(*r) for r in res)

    def get_newest_order_name(self) -> str:     #type: ignore
        """Получение последнего сканированного номера заказа"""
        with self.__s_con as con:
            con.cursor.execute('SELECT MAX(name) FROM Orders')
            return con.cursor.fetchone()[0]
