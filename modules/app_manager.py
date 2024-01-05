from os import name as osname
from typing import TYPE_CHECKING, Self, Literal


# Импорты для типизации менеджера
if TYPE_CHECKING:   
    from .descriptors import Descriptors
    from .data_base.library import Library
    from .data_base.log import Log
    from .gui.main import MainWindow
    from .trackers import OrdersTracker
    from .gui.frames.file_frame.processing_frame import ProcessingFrame
    from .gui.frames.file_frame.queue_frame import QueueFrame
    from .task_manager import TaskManager
    from data_base.settings import Settings



class _AppManager:
    """Класс собирающий в себя критические модули приложения"""

    __instance = None

    __slots__ = ('_os', '_desc', 'lib', 'log', 'mw', 'ot', 'pf', 'queue', 'tm', 'stg')
    
    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self._os: Literal['win', 'lin', 'other']
        self._desc: Descriptors
        self.lib: Library
        self.log: Log
        self.mw: MainWindow
        self.ot: OrdersTracker
        self.pf: ProcessingFrame        # Эти 2 фрейма будет записаны в мменеджер 
        self.queue: QueueFrame          # при инициализации основного окна
        self.tm: TaskManager
        self.stg: Settings


AppManager = _AppManager()


# Определяем тип ос
match osname:
    case 'nt': AppManager._os = 'win'
    case 'posix': AppManager._os = 'lin'
    case _: AppManager._os = 'other'


# Наполняем менеджер реальными объектами
# Порядок импортов важен
from .descriptors import Descriptors
AppManager._desc = Descriptors()

from .task_manager import TaskManager
AppManager.tm = TaskManager()

from .data_base.library import Library
AppManager.lib = Library()

from .trackers import OrdersTracker
AppManager.ot = OrdersTracker()

from .data_base.log import Log
AppManager.log = Log()

from .gui.main import MainWindow
AppManager.mw = MainWindow()   

from .data_base.settings import Settings
AppManager.stg = Settings()
