from modules.db_contextmanager import SafeConnect
from modules.app_manager import AppManagerW


__aLL__ = ('Logger', )


class Log(AppManagerW):
    """Класс предостовляющий доступ к чтению и записи лога заказов"""
    __s_con = SafeConnect('log.db')

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
