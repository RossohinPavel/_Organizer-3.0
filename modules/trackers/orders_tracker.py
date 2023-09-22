import os
import re
from modules.trackers.tracker import Tracker
from modules.order.tracker_proxies import *


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами заказов"""
    __orders = {}

    def get_tracker_settings(self):
        return self.app_m.Settings.autolog, self.app_m.TxtVars.orders_trk

    def manual(self):
        for proxy_lst in self.__orders.values():
            for proxy in proxy_lst:
                proxy.update_flag = True
        self.auto()

    def auto(self):
        self.app_m.ProcessingFrame.header.set('Трекер заказов')
        self.app_m.ProcessingFrame.qty.set('0/4')
        self.app_m.ProcessingFrame.pb['maximum'] = 4
        self.app_m.ProcessingFrame.pb['value'] = 0
        self.app_m.ProcessingFrame.status.set('Обновление списка заказов')
        self.__update_orders_dct()
        self.app_m.ProcessingFrame.qty.set('1/4')
        self.app_m.ProcessingFrame.pb['value'] += 1
        self.app_m.ProcessingFrame.status.set('Обновление списка тиражей')
        self.__update_edition_list()
        self.app_m.ProcessingFrame.qty.set('2/4')
        self.app_m.ProcessingFrame.pb['value'] += 1
        self.app_m.ProcessingFrame.status.set('Обновление объектов-тиражей')
        self.__update_proxies()
        self.app_m.ProcessingFrame.qty.set('3/4')
        self.app_m.ProcessingFrame.pb['value'] += 1
        self.app_m.ProcessingFrame.status.set('Сохранение информации')
        self.__update_log()
        self.app_m.ProcessingFrame.qty.set('4/4')
        self.app_m.ProcessingFrame.pb['value'] += 1

    def __update_orders_dct(self):
        """Обновление списка отслеживаемых заказов"""
        path = self.app_m.Settings.z_disc       # Получаем необходимые настройки
        limit = self.app_m.Settings.log_check_depth
        for proxy_obj in self.__orders:         # Помечаем все заказы на удаление
            proxy_obj.delete_flag = True        # При удачном сравнении прокси объект вернет состояние False
        for day in reversed(os.listdir(path)):
            if limit == 0:
                break
            if re.fullmatch(r'\d{4}(-\d{2}){2}', day):
                for order_name in reversed(os.listdir(f'{path}/{day}')):
                    if limit != 0 and re.fullmatch(r'\d{6}', order_name):
                        if order_name not in self.__orders:
                            self.__orders[OrderProxy(path, day, order_name)] = []
                        limit -= 1
        for obj in tuple(self.__orders):  # Очищаем словарь от заказов помеченных на удаление
            if obj.delete_flag:                  # В большинстве случаев - ограничено глубиной проверки лога
                del self.__orders[obj]           # Удалит из отслеживания удаленный вручную заказ

    def __update_edition_list(self):
        """Обновление списка отслеживаемых тиражей"""
        for order_proxy, proxies_lst in self.__orders.items():
            order_obj = order_proxy.order
            path = order_obj.path
            for name in os.listdir(path):
                if name not in proxies_lst:
                    if name == 'completed.htm':
                        proxies_lst.append(OrderInfoProxy(order_obj, path, name))
                    if name == 'PHOTO':
                        proxies_lst.append(PhotoProxy(order_obj, path, name))
                    if name != 'PHOTO' and os.path.isdir(f'{path}/{name}'):
                        proxies_lst.append(EditionProxy(order_obj, path, name))

    def __update_proxies(self):
        """Обновление информации в прокси объектах слежения"""
        for proxy_lst in self.__orders.values():
            for proxy in proxy_lst:
                proxy.update_info()

    def __update_log(self):
        """Отправляем в лог заказы, в которых обновилась информация"""
        lst = []
        for ord_proxy, proxy_lst in self.__orders.items():
            for proxy in proxy_lst:
                if proxy.update_flag:
                    lst.append(ord_proxy.order)
                    break
        self.app_m.Log.update_records(lst)
