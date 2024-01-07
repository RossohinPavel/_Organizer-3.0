# Импорты для работы самого AppManager'а
from os import name as osname
from typing import TYPE_CHECKING, Self


# Импорты внутренних модулей, которые не зависят 
# от менеджера или других внутренних модулей.
from . import descriptors
from .data_base import *


# Импорты для типизации менеджера
if TYPE_CHECKING:   
    from .gui.frames.file_frame.processing_frame import ProcessingFrame
    from .gui.frames.file_frame.queue_frame import QueueFrame


class _AppManager:
    """Класс собирающий в себя критические модули приложения"""

    __instance = None

    __slots__ = ('desc', 'lib', 'log', 'mw', 'ot', 'os', 'pf', 'queue', 'tm', 'stg')
    
    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.desc = descriptors
        self.lib = Library()
        self.log = Log()
        self.mw: MainWindow
        self.ot: OrdersTracker
        self.os = osname
        self.pf: ProcessingFrame        # Эти 2 фрейма будет записаны в мменеджер 
        self.queue: QueueFrame          # при инициализации основного окна
        self.tm: TaskManager
        self.stg: Settings


AppManager = _AppManager()


# Наполняем менеджер реальными объектами
from .task_manager import TaskManager
from .trackers import OrdersTracker
from .gui.main import MainWindow

AppManager.tm = TaskManager()
AppManager.ot = OrdersTracker()
AppManager.mw = MainWindow()   
AppManager.stg = Settings()
