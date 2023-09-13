import os
import time
from collections import Counter
from modules.trackers.tracker import Tracker


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами"""
    __cleaning_flag = False
    __observing_period = []
    __orders = []

    def get_settings(self):
        return self.app_m.Settings.autolog, self.app_m.TxtVars.orders_trk

    def main(self):
        limit = self.app_m.Settings.log_check_depth
        path = self.app_m.Settings.z_disc
        self.__update_period(limit, path)
        if self.__cleaning_flag:
            self.__clear_old_orders(limit)
        self.__update_orders(path)
        self.__update_log()

    def __update_period(self, limit, path):
        """Функция для обновления отслеживаемого периода"""
        for day in reversed(os.listdir(path)):
            if limit == 0:
                break
            if self.app_m.Constants.check_day(day):
                if day not in self.__observing_period:
                    self.__cleaning_flag = True
                    self.__observing_period.append(day)
                limit -= 1
                
    def __clear_old_orders(self, limit):
        """Функция для очистки отслеживаемого периода от старых дат с старых объектов заказов"""
        self.__observing_period = self.__observing_period[:limit]
        ind = 0
        while ind < len(self.__orders):
            if self.__orders[ind].creation_date not in self.__observing_period:
                del self.__orders[ind]
            ind += 1
        self.__cleaning_flag = False

    def __update_orders(self, path):
        """Функция для обновления списка отслеживаемых заказов"""
        for day in self.__observing_period:
            for order in os.listdir(f'{path}/{day}'):
                if order not in self.__orders and self.app_m.Constants.check_order(order):
                    self.__orders.insert(0, Order(path, day, order))

    def __update_log(self):
        """Получение информации из заказа и запись ее в лог"""
        pass


class Order:
    __slots__ = 'path', 'creation_date', 'name', 'content', '_counter'

    def __init__(self, path, creation_date, name):
        self.path = path
        self.creation_date = creation_date
        self.name = name
        self.content = tuple()
        self._counter = 0

    def get_content(self):
        return tuple()

    def update_info(self):
        pass

    def __eq__(self, other):
        res = other == self.name
        if res:
            print('Объект проверен')
        return res

    def __repr__(self):
        return f'{self.__class__.__name__}({self.creation_date}, {self.name})'
