from threading import Thread
from time import sleep as tsleep, time as ttime
from typing import Any, Callable, Type
from ..app_manager import AppManager


class Tracker:
    """Абстрактный класс реализующий общую логику работы трекера"""
    __slots__ = ('delay', 'appm', '__thread')

    class TrackerThread(Thread):
        """Параллельный поток, который запускает выполнение трекера в автоматическом режиме"""
        def __init__(self, tracker) -> None:
            self.tracker: Tracker = tracker
            self.is_repeating = True
            super().__init__(daemon=True)

        def run(self) -> None:
            """Зацикливает поток, запуская автоматический режим трекера"""
            while self.is_repeating:
                start = ttime()
                self.tracker.auto_init()
                tsleep(start - ttime() + self.tracker.delay)

    def __init__(self) -> None:
        self.delay = 150
        self.appm = AppManager
        self.__thread = self.TrackerThread(self)

        self.__class__.manual_init = self.__class__.__run_decorator(self.__class__.manual_init)   #type: ignore
        self.__class__.auto_init = self.__class__.__run_decorator(self.__class__.auto_init)       #type: ignore

    # Публичные ф-ии, используемые в дочерних классах
    def manual_init(self) -> None:
        """Запускает ручной режим работы трекера"""
        raise Exception('Функция manual не переопределена в дочерном классе')
    
    def auto_init(self) -> None:
        """Запускает трекер в автоматическом режиме."""
        raise Exception('Функция auto не переопределена в дочерном классе')
    
    @staticmethod
    def __run_decorator(func: Type[Callable[[Any], None]]) -> Callable[[Any], None]:
        """Декоратор для запуска трекера в менеджере задач"""
        def wrapper(instance: Any) -> None:
            AppManager.tm.create_task(func, instance)

        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    @property
    def auto(self) -> int:
        """Возвращает 1 или 0 в зависимости от того, включен автоматический режим трекера или нет"""
        return AppManager.stg.autolog
    
    @auto.setter
    def auto(self, value: int) -> None:
        """Включает или выключает автоматический режим трекера в зависимости от переданного значения"""
        match value:
            case 0:
                # Выключаем повторение на текущем потоке и перезаряжаем его))
                self.__thread.is_repeating = False
                self.__thread = self.TrackerThread(self)
            case _:
                self.__thread.start()
