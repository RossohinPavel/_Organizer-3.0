from datetime import datetime, timedelta
from ..tracker import Tracker
from ...file_iterators import ot_iterator
from .tracker_proxies import *


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами заказов"""
    __slots__ = 'orders', 'proxies', 'border_name'

    def __init__(self) -> None:
        super().__init__()
        self.orders: dict[str, OrderInfoProxy] = {}
        self.proxies: set[EditionProxy | PhotoProxy] = set()
        self.border_name = self.appm.log.get_newest_order_name()

        # Получаем значения из настроек и запускаем автолог
        self.auto = self.appm.stg.autolog

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
        for proxy in self.proxies: proxy.trackable = True
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

            # Вспомогательная переменная order_path
            order_path = f'{z_disc}/{day}/{order}'

            # Создаем прокси объект для заказа, которого нет в словаре self.orders
            if order not in self.orders:
                self.orders[order] = OrderInfoProxy(order_path, day, order)

            # Итерируемся по именам содержимого
            for name in contents:
                obj_name = order + name

                # Перед добавлением проверяем, есть ли эти объекты во множествах
                if obj_name not in self.proxies:
                    obj = PhotoProxy if name == 'PHOTO' else EditionProxy
                    self.proxies.add(obj(self.orders[order], order_path, name))
            
            # Уменьшаем лимит, если имя заказа меньше рубежного
            if order <= self.border_name:
                limit -= 1
        
        self.appm.pf.filebar.step_end()

    def __update_proxies(self):
        """Обновление информации в прокси объектах слежения"""
        self.appm.pf.filebar.maximum(len(self.proxies) + len(self.orders), 85)
        
        # Обновляем информацию в прокси объектах информации о заказе
        self.appm.pf.operation.step('Обновление объектов заказов')
        for order_proxy in self.orders.values():
            self.appm.pf.filebar.step(order_proxy.order)
            order_proxy.update_info()
            self.appm.pf.filebar.step_end()

        # Обновляем информацию в прокси объектах тиражей
        self.appm.pf.operation.step('Обновление объектов тиражей')
        for proxy in self.proxies:
            self.appm.pf.filebar.step(proxy.name)
            proxy.update_info()
            self.appm.pf.filebar.step_end()

    def __update_log(self):
        """Отправляем в лог заказы, в которых обновилась информация"""
        self.appm.pf.operation.step('Сохранение информации')
        self.appm.pf.filebar.maximum(1, 5)

        # Вызываем обновление лога.  
        self.appm.pf.filebar.step('Запись в лог файл')
        self.appm.log.update_records(self.proxies)
        self.appm.pf.filebar.step_end()

    def __clearing_orders(self):
        """
            Очистка self.orders и self.proxies от старых объектов, которые вышли за границу глубины проверки.
            Удалит только те заказы, прокси объекты которых не находятся в статусе отслеживаемых
        """
        self.appm.pf.operation.step('Очитска списка')
        self.appm.pf.filebar.maximum(1, 5)
        self.appm.pf.filebar.step('Удаляем старые объекты')

        # Устананвливаем границу на последний сканированный заказ
        self.border_name = max(self.orders)

        # Очищаем словарь self.orders и формируем вспомогательную переменную для очитски
        orders_to_del = set(self.orders.pop(x) for x in sorted(self.orders)[:-self.appm.stg.log_check_depth])
        
        # Получаем неотслеживаемы прокси объекты и вычитаем их из исходного множества
        self.proxies -= set(x for x in self.proxies if x.info_proxy in orders_to_del and not x.trackable)

        self.appm.pf.filebar.step_end()
