from threading import Thread
from time import sleep as tsleep, time as ttime
from typing import Any, Callable, Type, NoReturn
from appmanager import AppManager


class Tracker:
    """Абстрактный класс реализующий общую логику работы трекера"""
    __slots__ = ('delay', 'appm', '__thread')

    class TrackerThread(Thread):
        """Параллельный поток, который запускает выполнение трекера в автоматическом режиме"""
        def __init__(self, tracker):
            self.tracker: Tracker = tracker
            self.is_repeating = True
            super().__init__(daemon=True)

        def run(self) -> None:
            """Зацикливает поток, запуская автоматический режим трекера"""
            while self.is_repeating:
                start = ttime()
                self.tracker.auto()
                tsleep(start - ttime() + self.tracker.delay)

    def __init__(self) -> None:
        self.delay = 150
        self.appm = AppManager
        self.__thread = self.TrackerThread(self)
    
    def init_auto(self, value) -> None:
        """Запуск и остановка автоматического режима трекера"""
        if value:
            self.__thread.start()
        else:
            self.__thread.is_repeating = False
            self.__thread = self.TrackerThread(self)
    
    @staticmethod
    def run_decorator(func: Type[Callable[[Any], None]]) -> Callable[[Any], None]:
        """Декоратор для запуска трекера в менеджере задач"""
        def wrapper(instance) -> None:
            AppManager.tm.create_task(func, instance)
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    def _run(self) -> NoReturn:
        """Абстрактная ф-я. В дочернем классе реализует общую логику работы трекера"""
        raise Exception('Функция _run не переопределена в дочерном классе')

    @run_decorator
    def manual(self) -> None:
        """Запускает трекер в ручном режиме."""
        self._manual()

    def _manual(self) -> NoReturn:
        """Абстрактная ф-я. Реализует логику работы трекера в ручном режиме. Должна запускать ф-ю _run"""
        raise Exception('Функция manual не переопределена в дочерном классе')

    @run_decorator
    def auto(self) -> None:
        """Запускает трекер в автоматическом режиме."""
        raise Exception('Функция auto не переопределена в дочерном классе')

    def _auto(self) -> NoReturn:
        """Абстрактная ф-я. Реализует логику работы трекера в автоматическом режиме. Должна запускать ф-ю _run"""
        raise Exception('Функция auto не переопределена в дочерном классе')
