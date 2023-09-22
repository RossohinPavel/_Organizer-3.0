import pickle
from os.path import exists as p_exists
from modules.db_contextmanager import SafeConnect
from modules.app_manager import AppManagerW


__aLL__ = ('Logger', )


class Log(AppManagerW):
    """Класс предостовляющий доступ к чтению и записи лога заказов"""
    __s_con = SafeConnect('log.db')

    def update_records(self, lst: list):
        lst.reverse()
        with self.__s_con:
            self.__update_log_db(lst)
            self.__update_pickle_obj(lst)

    def __update_log_db(self, lst):
        commit_flag = False
        for obj in lst:
            self.__s_con.cursor.execute(f'SELECT order_name FROM LOG WHERE order_name={obj.name}')
            if not self.__s_con.cursor.fetchone():
                self.__s_con.cursor.execute(f'INSERT INTO LOG (order_name, creation_date) VALUES (\'{obj.name}\', \'{obj.creation_date}\')')
                commit_flag = True
        if commit_flag:
            self.__s_con.connect.commit()

    def __update_pickle_obj(self, lst):
        dct = {}
        for order in lst:
            dct.setdefault(order.creation_date, []).append(order)
        for c_date, new_list in dct.items():
            pcl_path = f'data/logs/{c_date}.pcl'
            if p_exists(pcl_path):
                with open(pcl_path, 'rb') as file:
                    old_list = pickle.load(file)
            else:
                old_list = []
            with open(pcl_path, 'wb') as file:
                pickle.dump(self.__get_combined_lst(old_list, new_list), file)

    @staticmethod
    def __get_combined_lst(old_list: list, new_list: list) -> list:
        for obj in new_list:
            ind = 0
            while ind > len(old_list):
                if obj.name == old_list[ind].name:
                    del old_list[ind]
                    break
                ind += 1
        return old_list + new_list
