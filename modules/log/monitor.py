import os
from threading import Thread, Lock

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
            self.__observing_update()  # Шаг 1 - Обновляем отслеживаемый период
        except:
            pass
        print(self.__observing_period)

    def __observing_update(self):
        """Функция для обновления отслеживаемого периода"""
        limit = self.app_m.stg.log_check_depth
        self.__observing_period.clear()
        new_period = reversed(os.listdir(self.app_m.stg.z_disc))
        for day in new_period:
            if limit == 0:
                break
            if self.app_m.cnst.check_day(day):
                if day not in self.__observing_period:
                    self.__observing_period.append(day)
                limit -= 1
