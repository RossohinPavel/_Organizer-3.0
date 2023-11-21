from datetime import datetime, timedelta
from ._tracker import Tracker
from grabbers import orders_grabber_iterator
from proxies.orders_tracker import *


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами заказов"""
    __slots__ = '_orders', '_border_name', '_z_disc', '_limit'

    def __init__(self):
        super().__init__()
        self._orders = {}
        self._z_disc: str
        self._limit: int
        self._border_name = self.appm.log.get_newest_order_name()

    def _run(self) -> None:
        # Получение значений атрибутов из настроек
        self._z_disc = self.appm.stg.z_disc
        self._limit = self.appm.stg.log_check_depth
        # Обновление инофрмации на Прогрессбаре
        self.appm.pf.header.set('Трекер заказов')
        self.appm.pf.filebar.maximum = 5
        # Проверяем наличие новых заказов
        self.appm.pf.operation.set('Обновление списка отслеживаемых заказов')
        self.appm.pf.filebar.set()
        self.__update_orders_dct()
        self.appm.pf.filebar += 1
        # self.storage.pf.status.set('2/5: Обновление списка отслеживаемых тиражей')
        # self.__update_edition_list()
        # self.storage.pf.pb['value'] += 1
        # self.storage.pf.status.set('3/5: Обновление информации')
        # self.__update_proxies()
        # self.storage.pf.pb['value'] += 1
        # self.storage.pf.status.set('4/5: Сохранение информации')
        # self.__update_log()
        # self.storage.pf.pb['value'] += 1
        # self.storage.pf.status.set('5/5: Очитска списка от старых заказов')
        # self.__clearing_orders()
        # self.storage.pf.pb['value'] += 1'
    
    def init_auto(self, value) -> None:
        if not value: 
            self.appm.txtvars.ot.set('Выключен')
        super().init_auto(value)

    def _manual(self):
        for proxy_lst in self._orders.values():
            for proxy in proxy_lst:
                proxy.update_flag = True
        self._run()

    def _auto(self):
        self.appm.txtvars.ot.set('Ожидание выполнения')
        current_time = datetime.now() + timedelta(seconds=self.delay)
        self._run()
        self.appm.txtvars.ot.set(f'Следующий скан: {current_time.strftime("%H:%M")}')

    def __update_orders_dct(self):
        """Обновление списка отслеживаемых заказов"""
        limit = self._limit
        for day, order in orders_grabber_iterator(self._z_disc):
            if limit == 0:
                break
            if order not in self._orders:
                self._orders[OrderDC(order, day)] = set()
            print(self._orders)
            if order <= self._border_name:
                limit -= 1


    # def __update_edition_list(self):
    #     """Обновление списка отслеживаемых прокси объектов тиражей и информации о заказе"""
    #     z_disc = self.storage.stg.z_disc                  # Получаем необходимые настройки
    #     for order_obj, proxies_lst in self.__orders.items():
    #         path = f'{z_disc}/{order_obj.creation_date}/{order_obj.name}'
    #         for name in listdir(path):
    #             if name not in proxies_lst:
    #                 if name == 'PHOTO':
    #                     proxies_lst.append(PhotoProxy(order_obj, path, name))
    #                     continue
    #                 if name == 'completed.htm':
    #                     proxies_lst.append(OrderInfoProxy(order_obj, path, name))
    #                     continue
    #                 if osp_isdir(f'{path}/{name}'):
    #                     proxies_lst.append(EditionProxy(order_obj, path, name))

    # def __update_proxies(self):
    #     """Обновление информации в прокси объектах слежения"""
    #     for proxy_lst in self.__orders.values():
    #         for proxy in proxy_lst:
    #             proxy.update_info()

    # def __update_log(self):
    #     """Отправляем в лог заказы, в которых обновилась информация"""
    #     lst = []
    #     for order_obj, proxy_lst in self.__orders.items():
    #         for proxy in proxy_lst:
    #             if proxy.update_flag:
    #                 lst.append(order_obj)
    #                 break
    #     if lst:     # Вызываем обновление лога если в списке не пустой.
    #         self.storage.Log.update_records(lst)

    # def __clearing_orders(self):
    #     """Очитска словаря от старых заказов, который вышли за границу глубины проверки.
    #     Удалит тольк те заказы, прокси объекты которых не находятся в статусе отслеживаемых"""
    #     names = sorted(x.name for x in self.__orders)
    #     self.border_name = names[-1]  # Устананвливаем границу на последний сканированный заказ
    #     for name in names[:-self.storage.stg.log_check_depth]:
    #         del_flag = True
    #         for proxi in self.__orders[name]:
    #             if proxi.update_flag:
    #                 del_flag = False
    #         if del_flag:
    #             del self.__orders[name]
