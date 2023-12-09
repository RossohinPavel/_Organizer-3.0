from datetime import datetime, timedelta
from ..tracker import Tracker
from ...grabbers import ot_grabber
from .proxy import *


class OrdersTracker(Tracker):
    """Основной объект слежения за файлами заказов"""
    __slots__ = 'proxies', 'border_name', 'z_disc', 'limit'

    def __init__(self):
        super().__init__()
        self.proxies = set()
        self.z_disc: str
        self.limit: int
        self.border_name = self.appm.log.get_newest_order_name()

    def _run(self) -> None:
        # Получение значений атрибутов из настроек
        self.z_disc = self.appm.stg.z_disc
        self.limit = self.appm.stg.log_check_depth

        # Обновление инофрмации на Прогрессбаре
        self.appm.pf.header.set('Трекер заказов')
        self.appm.pf.operation.maximum = 5

        # Проверяем наличие новых заказов
        self.__update_proxies()

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
            self.appm.ot_var.set('Выключен')
        super().init_auto(value)

    def _manual(self):
        # for proxy_lst in self._orders.values():
        #     for proxy in proxy_lst:
        #         proxy.update_flag = True
        self._run()

    def _auto(self):
        self.appm.ot_var.set('Ожидание выполнения')
        current_time = datetime.now() + timedelta(seconds=self.delay)
        self._run()
        self.appm.ot_var.set(f'Следующий скан: {current_time.strftime("%H:%M")}')

    def __update_proxies(self):
        """Обновление списка отслеживаемых заказов"""
        self.appm.pf.operation.set('Обновление списка отслеживаемых заказов')

        # Получаем лимит
        limit = self.limit

        # Итерируемся по заказам и их тиражам
        for day, order, contents in ot_grabber(self.z_disc):
            # прерываем цикл, когда лимит 0.
            if limit == 0: break

            # Итерируемся по именам содержимого
            for name in contents:
                # Если в отслеживаемых объектах есть это имя, то пропускаем их добавление
                if f'{order}_{name}' in self.proxies: continue

                # Создаем объекты, согласно их типу
                match name:
                    case 'PHOTO': pass
                    case 'completed.htm': pass
                    case _: pass
            
            # Уменьшаем лимит, если имя заказа меньше рубежного
            if order <= self.border_name:
                limit -= 1
        
        print(self.proxies)

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
