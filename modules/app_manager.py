from typing import TYPE_CHECKING, Self, Literal
from os import name as osname


# Импорты для типизации менеджера
if TYPE_CHECKING:   
    from .data_base import Library
    from .data_base import Log
    from gui.main import MainWindow
    from gui.frames import ProcessingFrame
    from ttkbootstrap import StringVar
    from task_manager import TaskManager
    from trackers.orders_tracker import OrdersTracker
    from .data_base import Settings


class _AppManager:
    """Класс собирающий в себя критические модули приложения"""
    __instance = None
    # Объявляем слоты для ускорения доступа
    __slots__ = ('SYSTEM', 'lib', 'log', 'mw', 'ot', 'ot_var', 'pf',  'tm', 'stg')
    
    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.SYSTEM: Literal['win', 'lin', 'other']
        self.lib: Library
        self.log: Log
        self.mw: MainWindow
        self.ot: OrdersTracker
        self.ot_var: StringVar
        self.pf: ProcessingFrame    # Этот фрейм будет записан в мменеджер при инициализации основного окна
        self.tm: TaskManager
        self.stg: Settings


AppManager = _AppManager()


# Определяем тип ос
match osname:
    case 'nt': AppManager.SYSTEM = 'win'
    case 'posix': AppManager.SYSTEM = 'lin'
    case _: AppManager.SYSTEM = 'other'


# Наполняем менеджер реальными объектами
from .data_base import Library
AppManager.lib = Library()

# from log import Log
# AppManager.log = Log()

from .task_manager import TaskManager
AppManager.tm = TaskManager()

# from trackers.orders_tracker import OrdersTracker
# AppManager.ot = OrdersTracker()

from .data_base import Settings
AppManager.stg = Settings()

from .gui.main import MainWindow
AppManager.mw = MainWindow()    # Самый последний инициализируемый модуль
