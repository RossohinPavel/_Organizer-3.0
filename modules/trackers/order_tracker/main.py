from datetime import datetime, timedelta
from ..tracker import Tracker, AppManager
from ...file_iterators import ot_iterator
from .tracker_proxies import *


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами заказов"""
    __slots__ = '_orders', '_proxies','_border_name'

    def __init__(self) -> None:
        super().__init__()
        self._orders: dict[str, OrderInfoProxy] = {}
        self._proxies: set[EditionProxy | PhotoProxy] = set()
        self._border_name = AppManager.log.get_newest_order_name()

        # Получаем значения из настроек и запускаем автолог
        AppManager._desc.autolog.add_call(self.auto)    #type: ignore

    def run(self) -> None:
        """Основная ф-я предостовляющая логику работы трекера"""
        # Обновление инофрмации на Прогрессбаре
        self.appm.pf.header.step('Трекер заказов')
        self.appm.pf.operation.maximum = 5

        # Основные шаги работы трекера
        self.__update_tracker()             # Обновление трекера, поиск новых тиражей
        self.__update_proxies()             # Обновление информации в объектах слежения
        self.__update_log()                 # Запись информации в лог
        self.__clearing_orders()            # Очитска списка от старых заказов

    def manual_init(self) -> None:
        # Принудительно переводим прокси объект в состояние ожидающих сканирования
        for proxy in self._proxies:
            proxy._count = 0
        self.run()

    def auto_init(self) -> None:
        self.appm.ot_var.set('Ожидание выполнения')
        current_time = datetime.now() + timedelta(seconds=self.delay)
        self.run()
        self.appm.ot_var.set(f'Следующий скан: {current_time.strftime("%H:%M")}')

    def __update_tracker(self) -> None:
        """Обновление списка отслеживаемых заказов"""
        # Установка значений в прогрессбар
        self.appm.pf.operation.step('Обновление трекера')
        self.appm.pf.filebar.maximum(1, 5)
        self.appm.pf.filebar.step('Поиск новых тиражей')

        # Получаем лимит и папку заказов
        limit = self.appm.stg.log_check_depth
        z_disc = self.appm.stg.z_disc

        # Итерируемся по заказам и их тиражам
        for day, order, contents in ot_iterator(z_disc):
            # Прерываем цикл, когда лимит 0.
            if limit == 0: break

            # Создаем прокси объект для заказа, которого нет в словаре self._orders
            if order not in self._orders:
                self._orders[order] = OrderInfoProxy(z_disc, day, order)
            
            # Получаем ссылки на Объект информации и на кортеж с прокси объектами тиражей
            info_proxy = self._orders[order]

            # Итерируемся по именам содержимого
            for name in contents:
                # Перед добавлением проверяем, есть ли эти объекты во множесте прокси объектоа
                proxy_name = order + name
                if proxy_name not in self._proxies:
                    obj = PhotoProxy if name == 'PHOTO' else EditionProxy
                    self._proxies.add(obj(info_proxy, proxy_name, name))
            
            # Уменьшаем лимит, если имя заказа меньше рубежного
            if order <= self._border_name:
                limit -= 1
        
        self.appm.pf.filebar.step_end()

    def __update_proxies(self):
        """Обновление информации в прокси объектах слежения"""
        self.appm.pf.filebar.maximum(len(self._proxies) + len(self._orders), 85)

        # Обновляем информацию в прокси объектах тиражей
        self.appm.pf.operation.step('Обновление тиражей')
        for proxy in self._proxies:
            self.appm.pf.filebar.step(proxy.name)
            proxy.update_proxy()
            self.appm.pf.filebar.step_end()
        
        # Обновляем информацию в прокси объектах информации о заказе
        self.appm.pf.operation.step('Обновление заказов')
        for order_proxy in self._orders.values():
            self.appm.pf.filebar.step(order_proxy.name)
            order_proxy.update_proxy()
            self.appm.pf.filebar.step_end()

    def __update_log(self):
        """Отправляем в лог заказы, в которых обновилась информация"""
        self.appm.pf.operation.step('Сохранение информации')
        self.appm.pf.filebar.maximum(1, 5)

        # Вызываем обновление лога.  
        self.appm.pf.filebar.step('Запись в лог файл')
        self.appm.log.update_records(self._proxies)
        self.appm.pf.filebar.step_end()

    def __clearing_orders(self):
        """
            Очистка self.orders и self.proxies от старых объектов, которые вышли за границу глубины проверки.
        """
        self.appm.pf.operation.step('Очитска списка')
        self.appm.pf.filebar.maximum(1, 5)
        self.appm.pf.filebar.step('Удаляем старые объекты')

        # Устананвливаем границу на последний сканированный заказ
        self._border_name = max(self._orders)

        # Очищаем словарь self.orders и формируем вспомогательную переменную для очитски
        orders_to_del = set()

        for order in sorted(self._orders)[:-self.appm.stg.log_check_depth]:
            del self._orders[order]
            orders_to_del.add(order)
        
        # Получаем неотслеживаемые прокси объекты и вычитаем их из исходного множества
        self._proxies -= set(x for x in self._proxies if x._order_proxy.name in orders_to_del)

        self.appm.pf.filebar.step_end()
