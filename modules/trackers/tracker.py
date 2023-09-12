from modules.app_manager import AppManager
from datetime import datetime, timedelta


class Tracker(AppManager):
    """Абстракнтый объект, предоставляющий основную логику слежения за файлами"""
    delay = 180

    def __init__(self):
        """Регистрирует цикл проверок Трекера, если соответсвующий трекер активен"""
        autorun, txt_var = self.get_settings()
        if autorun:
            self.app_m.IPlanner.create_loop(self.__update_txt_vars(txt_var, self.delay, self.__safe_run(self.main)), self.delay)

    @staticmethod
    def __safe_run(func):
        """Обертка для безопасного запуска функции"""
        def wrapper(*args, **kwargs):
            print('сработал cэйф ран')
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(e)
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    @staticmethod
    def __update_txt_vars(txt_var, delay, func):
        def wrapper(*args, **kwargs):
            txt_var.set('Ожидание выполнения')
            current_time = datetime.now() + timedelta(seconds=delay)
            func(*args, **kwargs)
            txt_var.set(f'Следующий скан: {current_time.strftime("%H:%M")}')
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    def get_settings(self):
        """Возвращает настройки автоматического запуска и текстовую переменную"""
        raise Exception('Функция get_settings не переопределена в дочерном классе')

    def run(self):
        """Функция предоставляющая возможность ручного создания основной задачи трекера"""
        self.app_m.IPlanner.create_task(self.__safe_run(self.main))

    def main(self):
        """Абстракная ф-я для сбора функций дочерних классов"""
        raise Exception('Функция main не переопределена в дочерном классе')
