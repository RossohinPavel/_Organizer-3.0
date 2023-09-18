from modules.app_manager import AppManager
from datetime import datetime, timedelta


class Tracker(AppManager):
    """Абстракнтый объект, предоставляющий основную логику слежения за файлами"""
    delay = 180

    def get_tracker_settings(self):
        """Возвращает настройки автоматического запуска и текстовую переменную"""
        raise Exception('Функция get_tracker_settings не переопределена в дочерном классе')

    def __init__(self):
        """Регистрирует цикл проверок Трекера, если соответсвующий трекер активен"""
        autorun, txt_var = self.get_tracker_settings()
        if autorun:
            self.app_m.IPlanner.create_loop(self.__update_txt_vars(txt_var, self.delay, self.auto), self.delay)

    def run(self):
        """Функция предоставляющая возможность ручного создания основной задачи трекера"""
        self.app_m.IPlanner.create_task(self.manual)

    def manual(self):
        """Абстрактная ф-я для сбора функций дочерних классов ручного управления трекером"""
        raise Exception('Функция manual для ручного управления трекером не переопределена в дочернем классе')

    def auto(self):
        """Абстракная ф-я для сбора функций дочерних классов"""
        raise Exception('Функция auto не переопределена в дочерном классе')

    @staticmethod
    def __update_txt_vars(txt_var, delay, func):
        """Обертка для изменения значений текстовых переменных задач"""
        def wrapper(*args, **kwargs):
            txt_var.set('Ожидание выполнения')
            current_time = datetime.now() + timedelta(seconds=delay)
            func(*args, **kwargs)
            txt_var.set(f'Следующий скан: {current_time.strftime("%H:%M")}')
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper
