import os
import time
from collections import Counter
from modules.trackers.tracker import Tracker


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами"""
    __orders = []

    def get_settings(self):
        return self.app_m.Settings.autolog, self.app_m.TxtVars.orders_trk

    def main(self):
        z_disc = self.app_m.Settings.z_disc
        period = tuple(self.__get_period(self.app_m.Settings.log_check_depth, z_disc, self.app_m.Constants.check_day))
        self.__update_orders_list(period, z_disc, self.app_m.Constants.check_order)
        self.__clear_old_orders(period)
        self.__update_orders_info()
        print(self.__orders)

    def __get_period(self, limit, z_disc, check_func):
        """Функция для получения отслеживаемого периода"""
        for day in reversed(os.listdir(z_disc)):
            if limit == 0:
                break
            if check_func(day):
                yield day
                limit -= 1

    def __update_orders_list(self, period, path, check_func):
        """Функция для обновления списка отслеживаемых заказов"""
        for day in period:
            for order in reversed(os.listdir(f'{path}/{day}')):
                if order not in self.__orders and check_func(order):
                    self.__orders.append(Order(path, day, order))
                
    def __clear_old_orders(self, period):
        """Функция для очистки старых объектов заказов"""
        ind = 0
        while ind < len(self.__orders):
            if self.__orders[ind].creation_date not in period:
                del self.__orders[ind]
            ind += 1

    def __update_orders_info(self):
        """Обновление информации в заказах и при необходимосте ее запись в лог"""
        pass


class Order:
    __slots__ = 'path', 'creation_date', 'name', 'content', '_counter'

    def __init__(self, path, creation_date, name):
        self.path = path
        self.creation_date = creation_date
        self.name = name

    def __eq__(self, other):
        return other == self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.creation_date}, {self.name})'
