from modules.db_contextmanager import SafeConnect
from modules.app_manager import AppManagerW


__aLL__ = ('Logger', )


class Log(AppManagerW):
    """Класс предостовляющий доступ к чтению и записи лога заказов"""
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
                self.__s_con.cursor.execute(f'UPDATE Orders set {req} WHERE name={values[0]}')
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
                self.__s_con.cursor.execute(f'UPDATE {table} set {req} WHERE order_name={values[0]} AND name=\'{values[1]}\'')
            else:
                self.__s_con.cursor.execute(f'INSERT INTO {table} {keys} VALUES {values}')


    # def get(self, order_name):
    #     """Функция для получения имени заказа и даты его создания"""
    #     with self.__s_con:
    #         return self.__check_order(order_name)
    #
    # def __check_order(self, order_name):
    #     """Проверка на присутсвие заказа в библиотеке. Использовать строго с контекстным менеджером"""
    #     self.__s_con.cursor.execute(f'SELECT order_name, creation_date FROM LOG WHERE order_name={order_name}')
    #     return self.__s_con.cursor.fetchone()
    #
    # def update_records(self, lst: list):
    #     """Сборная ф-я для обновления библиотеки"""
    #     lst.reverse()
    #     with self.__s_con:
    #         self.__update_log_db(lst)
    #         self.__update_pickle_obj(lst)
    #
    # def __update_log_db(self, lst):
    #     """Обновление базы данных SQLite"""
    #     commit_flag = False
    #     for obj in lst:
    #         if self.__check_order(obj.name) is None:
    #             self.__s_con.cursor.execute(f'INSERT INTO LOG (order_name, creation_date) VALUES (\'{obj.name}\', \'{obj.creation_date}\')')
    #             commit_flag = True
    #     if commit_flag:
    #         self.__s_con.connect.commit()
    #
    # @staticmethod
    # def __get_combined_lst(old_list: list, new_list: list) -> list:
    #     """Вспомогательная ф-я для получения комбинированного списка, где новые значения заменяют старые"""
    #     for obj in new_list:
    #         ind = 0
    #         while ind > len(old_list):
    #             if obj.name == old_list[ind].name:
    #                 del old_list[ind]
    #                 break
    #             ind += 1
    #     return old_list + new_list
