from ._safe_connect import SafeConnect
from .app_manager import AppManager
from modules.orders_repr.base_dataclasses import *


__aLL__ = ('Log', )


class Log:
    """Класс предостовляющий доступ к чтению и записи лога заказов"""
    storage = AppManager.storage
    __new__ = AppManager.write_to_storage('log')
    __s_con = SafeConnect('log.db')

    def update_records(self, lst: list):
        """Сборная ф-я для обновления библиотеки"""
        lst.reverse()
        with self.__s_con:
            self.__update_orders_table(lst)
            self.__s_con.connect.commit()

    def __update_orders_table(self, lst):
        """Обновление данных в основной таблице информации о заказе"""
        for order_dc in lst:
            keys, values = zip(*((k, v) for k, v in order_dc.__dict__.items() if k not in ('photo', 'content')))
            self.__s_con.cursor.execute(f'SELECT EXISTS (SELECT name FROM Orders WHERE name={order_dc.name} LIMIT 1)')
            if self.__s_con.cursor.fetchone()[0]:
                req = ', '.join(f'{keys[x]} = \'{values[x]}\'' for x in range(2, 5))
                self.__s_con.cursor.execute(f'UPDATE Orders SET {req} WHERE name={values[0]}')
            else:
                self.__s_con.cursor.execute(f'INSERT INTO Orders {keys} VALUES {values}')
            self.__update_editions_tables(*order_dc.content, *order_dc.photo)

    def __update_editions_tables(self, *edt_tuple):
        """Обновление данных в таблице тиражей"""
        for edt in edt_tuple:
            table = 'Editions' if edt.__class__.__name__ == 'Edition' else 'Photos'
            keys, values = zip(*((k, v) for k, v in edt.__dict__.items() if v is not None))
            self.__s_con.cursor.execute(f'SELECT EXISTS(SELECT name FROM {table} WHERE order_name={values[0]} AND name=\'{values[1]}\' LIMIT 1)')
            if self.__s_con.cursor.fetchone()[0]:
                req = ', '.join(f'{keys[x]} = \'{values[x]}\'' for x in range(2, len(keys)))
                self.__s_con.cursor.execute(f'UPDATE {table} SET {req} WHERE order_name={values[0]} AND name=\'{values[1]}\'')
            else:
                self.__s_con.cursor.execute(f'INSERT INTO {table} {keys} VALUES {values}')

    def get(self, order_name):
        """Получение объекта заказа из лога. Возвращает объект - датакласс заказа или None, если заказа нет"""
        with self.__s_con:
            self.__s_con.cursor.execute(f'SELECT * FROM Orders WHERE name={order_name}')
            res = self.__s_con.cursor.fetchone()
            if res:
                order = Order(*res[1:])
                self.__get_edition(order)
                return order

    def __get_edition(self, order):
        """Вспомогательная ф-я для наделения объекта заказа объектами тиражей"""
        for table in ('Editions', 'Photos'):
            self.__s_con.cursor.execute(f'SELECT * FROM {table} WHERE order_name={order.name}')
            res = tuple(eval(f'{table[:-1]}(*{x[1:]})') for x in self.__s_con.cursor.fetchall())
            if res:
                if table == 'Photos':
                    order.photo = res
                else:
                    order.content = res

    def get_newest_order_name(self) -> str:
        with self.__s_con as con:
            con.cursor.execute('SELECT MAX(name) FROM Orders')
            return con.cursor.fetchone()[0]
