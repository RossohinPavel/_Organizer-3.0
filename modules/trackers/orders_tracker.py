from os import listdir
from os.path import isdir as osp_isdir
from datetime import datetime, timedelta
from ..grabbers import OrdersGrabberIterator
from ._tracker import Tracker
from modules.orders_repr.orders_tracker_proxies import *


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами заказов"""
    __orders = {}

    def __init__(self):
        super().__init__()
        self.border_name = self.storage.log.get_newest_order_name()

    def run(self):
        self.storage.pf.header.set('Трекер заказов')
        self.storage.pf.pb['maximum'] = 5
        self.storage.pf.status.set('1/5: Обновление списка отслеживаемых заказов')
        self.__update_orders_dct()
        self.storage.pf.pb['value'] += 1
        self.storage.pf.status.set('2/5: Обновление списка отслеживаемых тиражей')
        self.__update_edition_list()
        self.storage.pf.pb['value'] += 1
        self.storage.pf.status.set('3/5: Обновление информации')
        self.__update_proxies()
        self.storage.pf.pb['value'] += 1
        self.storage.pf.status.set('4/5: Сохранение информации')
        self.__update_log()
        self.storage.pf.pb['value'] += 1
        self.storage.pf.status.set('5/5: Очитска списка от старых заказов')
        self.__clearing_orders()
        self.storage.pf.pb['value'] += 1
        print(len(self.__orders))

    def manual(self):
        for proxy_lst in self.__orders.values():
            for proxy in proxy_lst:
                proxy.update_flag = True
        self.run()

    def auto(self):
        self.storage.txt_vars.orders_trk.set('Ожидание выполнения')
        current_time = datetime.now() + timedelta(seconds=self.delay)
        self.run()
        self.storage.txt_vars.orders_trk.set(f'Следующий скан: {current_time.strftime("%H:%M")}')

    def __update_orders_dct(self):
        """Обновление списка отслеживаемых заказов"""
        path = self.storage.stg.z_disc              # Получаем необходимые настройки
        limit = self.storage.stg.log_check_depth
        for day, order in OrdersGrabberIterator(path):
            if limit == 0:
                break
            if order not in self.__orders:
                self.__orders[Order(order, day)] = []
            if order <= self.border_name:
                limit -= 1

    def __update_edition_list(self):
        """Обновление списка отслеживаемых прокси объектов тиражей и информации о заказе"""
        z_disc = self.storage.stg.z_disc                  # Получаем необходимые настройки
        for order_obj, proxies_lst in self.__orders.items():
            path = f'{z_disc}/{order_obj.creation_date}/{order_obj.name}'
            for name in listdir(path):
                if name not in proxies_lst:
                    if name == 'PHOTO':
                        proxies_lst.append(PhotoProxy(order_obj, path, name))
                        continue
                    if name == 'completed.htm':
                        proxies_lst.append(OrderInfoProxy(order_obj, path, name))
                        continue
                    if osp_isdir(f'{path}/{name}'):
                        proxies_lst.append(EditionProxy(order_obj, path, name))

    def __update_proxies(self):
        """Обновление информации в прокси объектах слежения"""
        for proxy_lst in self.__orders.values():
            for proxy in proxy_lst:
                proxy.update_info()

    def __update_log(self):
        """Отправляем в лог заказы, в которых обновилась информация"""
        lst = []
        for order_obj, proxy_lst in self.__orders.items():
            for proxy in proxy_lst:
                if proxy.update_flag:
                    lst.append(order_obj)
                    break
        if lst:     # Вызываем обновление лога если в списке не пустой.
            self.storage.Log.update_records(lst)

    def __clearing_orders(self):
        """Очитска словаря от старых заказов, который вышли за границу глубины проверки.
        Удалит тольк те заказы, прокси объекты которых не находятся в статусе отслеживаемых"""
        names = sorted(x.name for x in self.__orders)
        self.border_name = names[-1]  # Устананвливаем границу на последний сканированный заказ
        for name in names[:-self.storage.stg.log_check_depth]:
            del_flag = True
            for proxi in self.__orders[name]:
                if proxi.update_flag:
                    del_flag = False
            if del_flag:
                del self.__orders[name]
