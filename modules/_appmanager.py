from typing import TYPE_CHECKING, Self


if TYPE_CHECKING:   # Здесь пишем импорты для типизации менеджера
    from .library import Library
    from .log import Log
    from .gui.main import MainWindow
    from .gui.frames import ProcessingFrame
    from tkinter import StringVar
    from .task_manager import TaskManager
    from .settings import Settings


class AppManagerStorage:
    """Класс собирающий в себя критические модули приложения"""
    # Объявляем слоты для ускорения доступа
    __slots__ = 'lib', 'log', 'mw', 'orders_trk', 'pf', 'tm', 'stg'
    __instance = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.lib: Library
        self.log: Log
        self.mw: MainWindow
        self.pf: ProcessingFrame    # Этот фрейм будет записан в мменеджер при инициализации основного окна
        self.orders_trk: StringVar
        self.tm: TaskManager
        self.stg: Settings


AppManager = AppManagerStorage()


 # Наполняем менеджер реальными объектами
from .library import Library
AppManager.lib = Library()
from .log import Log
AppManager.log = Log()
from .gui.main import MainWindow
AppManager.mw = MainWindow()
from .task_manager import TaskManager
AppManager.tm = TaskManager()
from .settings import Settings
AppManager.stg = Settings()     # Самый последний инициализируемый модуль
