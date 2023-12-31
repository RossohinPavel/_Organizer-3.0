from typing import TYPE_CHECKING, Self, Literal
from os import name as osname


# Импорты для типизации менеджера
if TYPE_CHECKING:   
    from .data_base import Library
    from .data_base import Log
    from .gui.main import MainWindow
    from .trackers import OrdersTracker
    # from .gui.frames import ProcessingFrame
    from .gui.frames.file_frame.queue_frame import QueueFrame
    from .task_manager import TaskManager
    from .data_base import Settings


class _AppManager:
    """Класс собирающий в себя критические модули приложения"""

    __instance = None

    __slots__ = ('SYSTEM', 'lib', 'log', 'mw', 'ot', 'pf', 'queue', 'tm', 'stg')
    
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
        # self.pf: ProcessingFrame      # Эти 2 фрейма будет записаны в мменеджер 
        self.queue: QueueFrame          # при инициализации основного окна
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

from .data_base import Log
AppManager.log = Log()

from .task_manager import TaskManager
AppManager.tm = TaskManager()

from .gui.main import MainWindow
AppManager.mw = MainWindow()   

# from .trackers import OrdersTracker
# AppManager.ot = OrdersTracker()

from .data_base import Settings
AppManager.stg = Settings()
