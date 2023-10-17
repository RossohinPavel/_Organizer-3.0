from threading import Thread
from time import sleep
from ..app_manager import AppManager


class TrackerThread(Thread):
    """Параллельный поток, который запускает выполнение трекера в автоматическом режиме"""
    def __init__(self, tracker):
        self.tracker = tracker
        self.stop = False
        super().__init__(daemon=True)

    def run(self):
        while not self.stop:
            self.tracker.auto()
            sleep(self.tracker.delay)


@AppManager
class Tracker:
    """Абстрактный класс реализующий общую логику работы трекера"""
    delay = 180

    def __init__(self):
        self.__thread = TrackerThread(self)
        self.manual = self.__run_decorator(self.manual)
        self.auto = self.__run_decorator(self.auto)

    def run(self):
        """Абстрактная ф-я. В дочернем классе реализует общую логику работы трекера"""
        raise Exception('Функция run не переопределена в дочерном классе')

    def manual(self):
        """Абстрактная ф-я. В дочернем классе предоставляет возможность запуска трекера в ручном режиме"""
        raise Exception('Функция manual не переопределена в дочерном классе')

    def auto(self):
        """Абстрактная ф-я. В дочернем классе предоставляет возможность запуска трекера в автоматическом режиме"""
        raise Exception('Функция auto не переопределена в дочерном классе')

    def __run_decorator(self, func):
        """Декоратор для запуска трекера в менеджере задач"""
        def wrapper(*args, **kwargs):
            self.storage.tm.create_task(func, args, kwargs)

        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    def init_auto(self, value):
        """Запуск и остановка автоматического режима трекера"""
        if value:
            self.__thread.start()
        else:
            self.__thread.stop = True
            self.__thread = TrackerThread(self)
