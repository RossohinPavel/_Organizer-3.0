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
        self.__update_orders_list(period, z_disc, self.app_m.Constants)
        self.__clear_old_orders(period)
        self.__update_orders_info()

    def __get_period(self, limit, z_disc, check_func):
        """Функция для получения отслеживаемого периода"""
        for day in reversed(os.listdir(z_disc)):
            if limit == 0:
                break
            if check_func(day):
                yield day
                limit -= 1

    def __update_orders_list(self, period, z_disc, constants):
        """Функция для обновления списка отслеживаемых заказов"""
        for day in period:
            for order in reversed(os.listdir(f'{z_disc}/{day}')):
                if order not in self.__orders and constants.check_order(order):
                    self.__orders.append(Order(constants, z_disc, day, order))
                
    def __clear_old_orders(self, period):
        """Функция для очистки старых объектов заказов"""
        ind = 0
        while ind < len(self.__orders):
            if self.__orders[ind].creation_date not in period:
                del self.__orders[ind]
            ind += 1

    def __update_orders_info(self):
        """Обновление информации в заказах и при необходимосте ее запись в лог"""
        lst = []
        for order in self.__orders:
            order.update_content()
            for content in order.content:
                if content.info_flag:
                    lst.append(content.info)
        print(*lst, sep='\n')


class Order:
    __slots__ = 'constants', 'z_disc', 'creation_date', 'name', 'content'

    def __init__(self, constants, z_disc, creation_date, name):
        self.constants = constants
        self.z_disc = z_disc
        self.creation_date = creation_date
        self.name = name
        self.content = []

    def update_content(self):
        path = f'{self.z_disc}/{self.creation_date}/{self.name}'
        for name in os.listdir(path):
            if name not in self.content:
                if os.path.isdir(f'{path}/{name}'):
                    if name == 'PHOTO':
                        self.content.append(PhotoEdition(self, name))
                    else:
                        self.content.append(Edition(self, name))
                if name == 'completed.htm':
                     self.content.append(OrderInfo(self, name))

    def __eq__(self, other):
        return other == self.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.creation_date}, {self.name})'


class Base:
    __slots__ = 'order_obj', 'name', 'info', 'info_flag', '_counter'
    
    def __init__(self, order_obj, name):
        self.order_obj = order_obj
        self.name = name
        self.info = None
        self.info_flag = False
        self._counter = 0
        self.__update_info()

    def __update_info(self):
        if self._counter == 0:
            res = self.get_info()
            if self.info != res:
                self.info = res
                self.info_flag = True
            else:
                self.info_flag = False
                self._counter = 20
        else:
            self._counter -= 1

    def get_info(self):
        raise Exception('функция get_info не переопределена в дочернем классе')

    def __eq__(self, other):
        res = self.name == other
        if res:
            self.__update_info()
        return res

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.name}>'


class Edition(Base):
    def get_info(self):
        pass


class PhotoEdition(Base):
    paper_type = {'Глянцевая': 'Fuji Gl', 'Матовая': 'Fuji Mt'}
    
    def get_info(self):
        path = f'{self.order_obj.z_disc}/{self.order_obj.creation_date}/{self.order_obj.name}/PHOTO/_ALL/Фотопечать'
        photo_dct = {}
        for paper in os.listdir(path):
            for form in os.listdir(f'{path}/{paper}'):
                paper_format, multiplier = form[5:].split('--')
                name = f'{self.paper_type.get(paper, "Fuji ???")} {paper_format}'
                photo_dct[name] = photo_dct.get(name, 0) + len(os.listdir(f'{path}/{paper}/{form}')) * int(multiplier)
        return photo_dct


class OrderInfo(Base):
    def get_info(self):
        pass
