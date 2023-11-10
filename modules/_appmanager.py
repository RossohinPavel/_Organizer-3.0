from typing import TYPE_CHECKING, Self


__all__ = ('AppManager', )


if TYPE_CHECKING:   # Здесь пишем импорты для типизации менеджера
    from .library import Library
    from .gui.main import MainWindow
    from tkinter import StringVar
    from .gui.frames import ProcessingFrame
    from .settings import Settings


class AppManagerStorage:
    """Класс собирающий в себя критические модули приложения"""
    # Объявляем слоты для ускорения доступа
    __slots__ = 'lib', 'mw', 'orders_trk', 'pf', 'stg'
    __instance = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.lib: Library
        self.mw: MainWindow
        self.pf: ProcessingFrame
        self.orders_trk: StringVar
        self.stg: Settings


AppManager = AppManagerStorage()


 # Наполняем менеджер реальными объектами
from .library import Library
AppManager.lib = Library()
from .gui.main import MainWindow
AppManager.mw = MainWindow()
from .settings import Settings
AppManager.stg = Settings()     # Самый последний инициализируемый модуль
