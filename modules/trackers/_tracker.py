from threading import Thread
from time import sleep as tsleep, time as ttime
from ..app_manager import AppManager


class Tracker:
    """
        Абстрактный класс реализующий общую логику работы трекера.
        Публичные ф-ии используются для запуска трекера 
        в автоматическом (auto_init) или ручном режимах (manual_init).
        Логику работы нужно прописывать в защищенных функциях, 
        имена которых начинаются с нижнего подчеркивания.
    """

    __slots__ = ('delay', '__thread')

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
        # Стандартный цикл работы трекера в 150 секунд - 2,5 минуты
        self.delay = 150

        # Поток, в котором запускается автоматическая функция трекера
        self.__thread = self.TrackerThread(self)

    def auto_init(self) -> None:
        """
            Публичная ф-я. Создает задачу в менеджере задач.
            Запускает ф-ю _auto_init - реализующую логику работы 
            трекера в автоматическом режиме.
        """
        AppManager.tm.create_task(self._auto_init)  #type: ignore

    def _auto_init(self) -> None:
        """Логика работы трекера в автоматическом режиме"""
        raise Exception('Функция _auto_init не переопределена в дочерном классе')

    def manual_init(self) -> None:
        """
            Публичная ф-я. Создает задачу в менеджере задач.
            Запускает ф-ю _manual_init - реализующую логику работы 
            трекера в ручном режиме.
        """
        AppManager.tm.create_task(self._manual_init)  #type: ignore

    def _manual_init(self) -> None:
        """Запускает ручной режим работы трекера"""
        raise Exception('Функция manual не переопределена в дочерном классе')

    def auto(self, value: int) -> None:
        """Включает или выключает автоматический режим трекера в зависимости от переданного значения"""
        match value:
            case 0:
                # Выключаем повторение на текущем потоке и перезаряжаем его))
                self.__thread.is_repeating = False
                self.__thread = self.TrackerThread(self)
            case _:
                self.__thread.start()
