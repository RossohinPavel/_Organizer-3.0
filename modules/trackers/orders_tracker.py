import os
import time
from modules.trackers.tracker import Tracker


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами"""
    __observing_period = []
    __orders = []

    def get_settings(self):
        return self.app_m.Settings.autolog, self.app_m.TxtVars.orders_trk

    def main(self):
        path = self.app_m.Settings.z_disc
        self.__update_period(path)
        self.__update_orders(path)
        self.__update_log()

    def __update_period(self, path):
        """Функция для обновления отслеживаемого периода"""
        limit = self.app_m.Settings.log_check_depth
        self.__observing_period.clear()
        new_period = reversed(os.listdir(path))
        for day in new_period:
            if limit == 0:
                break
            if self.app_m.Constants.check_day(day):
                if day not in self.__observing_period:
                    self.__observing_period.append(day)
                limit -= 1

    def __update_orders(self, path):
        """Функция для обновления списка отслеживаемых заказов"""
        for day in self.__observing_period:
            for order in os.listdir(f'{path}/{day}'):
                if order not in self.__orders and self.app_m.Constants.check_order(order):
                    self.__orders.insert(0, Order(day, order))

    def __update_log(self):
        """Получение информации из заказа и запись ее в лог"""
        pass


class Order:
    __slots__ = 'creation_date', 'name'

    def __init__(self, creation_date, name):
        self.creation_date = creation_date
        self.name = name
        print('объект создан')

    def update_info(self):
        pass

    def __eq__(self, other):
        res = other == self.name
        if res:
            print('Объект проверен')
        return res

    def __repr__(self):
        return f'{self.__class__.__name__}({self.creation_date}, {self.name})'
