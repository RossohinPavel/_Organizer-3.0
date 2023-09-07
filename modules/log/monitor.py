import os
from threading import Thread, Lock
from tkinter import messagebox as tkmb

__all__ = ('Monitor', )


class Monitor:
    """Основной объект слежения за файлами"""
    __instance = None
    __txt_vars_lock = Lock()
    __observing_period = []
    __orders = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, app_m):
        self.app_m = app_m

    def run(self):
        """Запускает сканирование лога"""
        self.app_m.pln.create_task(self.__main)

    def __main(self):
        self.app_m.txt_vars.mnt_status.set('Сканирую на наличие новых заказов')
        try:
            path = self.app_m.stg.z_disc
            self.__update_period(path)  # Шаг 1 - Обновляем отслеживаемый период
            self.__update_orders(path)
        except Exception as e:
            tkmb.showinfo(message=e)
        print(self.__observing_period)
        print(self.__orders)

    def __update_period(self, path):
        """Функция для обновления отслеживаемого периода"""
        limit = self.app_m.stg.log_check_depth
        self.__observing_period.clear()
        new_period = reversed(os.listdir(path))
        for day in new_period:
            if limit == 0:
                break
            if self.app_m.cnst.check_day(day):
                if day not in self.__observing_period:
                    self.__observing_period.append(day)
                limit -= 1

    def __update_orders(self, path):
        """Функция для обновления списка отслеживаемых заказов"""
        for day in self.__observing_period:
            for order in os.listdir(f'{path}/{day}'):
                if order not in self.__orders and self.app_m.cnst.check_order(order):
                    self.__orders.insert(0, Order(day, order))
            


class Order:
    __slots__ = 'creation_date', 'name'

    def __init__(self, creation_date, name):
        self.creation_date = creation_date
        self.name = name
        print('объект создан')

    def __eq__(self, other):
        res = other == self.name
        if res:
            print('Объект проверен')
        return res

    def __repr__(self):
        return f'{self.__class__.__name__}({self.creation_date}, {self.name})'


if __name__ == '__main__':
    tkmb.showinfo(message='test')
