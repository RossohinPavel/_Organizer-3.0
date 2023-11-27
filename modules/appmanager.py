from typing import TYPE_CHECKING, Any, Self, Literal, Type
import os


# Импорты для типизации менеджера
if TYPE_CHECKING:   
    from library import Library
    from log import Log
    from gui.main import MainWindow
    from gui.frames import ProcessingFrame
    from ttkbootstrap import StringVar, IntVar
    from task_manager import TaskManager
    from trackers.orders_tracker import OrdersTracker
    from settings import Settings


class _TxtVars:
    """Класс для хранения переменных для виджетов"""
    __slots__ = 'ot', 'queue'
    
    def __init__(self) -> None:
        self.ot: StringVar
        self.queue: IntVar


class _AppManager:
    """Класс собирающий в себя критические модули приложения"""
    # Объявляем слоты для ускорения доступа
    __slots__ = 'SYSTEM', 'lib', 'log', 'mw', 'pf', 'tm', 'txtvars', 'stg', 'ot'
    __instance = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.SYSTEM: Literal['win', 'lin', 'other']
        self.lib: Library
        self.log: Log
        self.mw: MainWindow
        self.pf: ProcessingFrame    # Этот фрейм будет записан в мменеджер при инициализации основного окна
        self.txtvars = _TxtVars()
        self.tm: TaskManager
        self.ot: OrdersTracker
        self.stg: Settings


AppManager = _AppManager()


# Определяем тип ос
match os.name:
    case 'nt': AppManager.SYSTEM = 'win'
    case 'posix': AppManager.SYSTEM = 'lin'
    case _: AppManager.SYSTEM = 'other'


# Наполняем менеджер реальными объектами
# from library import Library
# AppManager.lib = Library()
# from log import Log
# AppManager.log = Log()
# from task_manager import TaskManager
# AppManager.tm = TaskManager()
# from trackers.orders_tracker import OrdersTracker
# AppManager.ot = OrdersTracker()
from settings import Settings
AppManager.stg = Settings()     
from gui.main import MainWindow
AppManager.mw = MainWindow()    # Самый последний инициализируемый модуль


