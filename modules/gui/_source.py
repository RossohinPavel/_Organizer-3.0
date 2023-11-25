import tkinter
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
from typing import Callable, NamedTuple, Any, Mapping, Type
from appmanager import AppManager


class Geometry(NamedTuple):
    """Для описании геометрии окон, фреймов и т.д."""
    width: int
    height: int


class ChildWindow(tb.Toplevel):
    """Конструктор для дочерних окон"""
    WIN_GEOMETRY = Geometry(100, 100)
    LIN_GEOMETRY = Geometry(100, 100)

    # Размечаем окно согласно выбранной ОС
    match AppManager.SYSTEM:
        case 'win': _geometry = WIN_GEOMETRY
        case 'lin' | _: _geometry = LIN_GEOMETRY

    # Переменная для хранения имени окна
    win_title = None

    # Список обязательных атирбутов для инициализации tb.Toplevel
    __TK_KWARGS = ('title', 
                   'iconphoto', 
                   'size', 
                   'position', 
                   'minsize', 
                   'maxsize', 
                   'resizable', 
                   'transient', 
                   'overrideredirect', 
                   'windowtype', 
                   'topmost', 
                   'toolwindow', 
                   'alpha')
    
    def __init__(self, master: tkinter.Misc, /, **kwargs: Mapping[str, Any]) -> None:
        title = self.win_title if self.win_title else self.__class__.__name__
        # Фильтруем атрибуты, чтобы лишние не были переданы в инициализатор окна
        my_kwargs = {x: y for x, y in kwargs.items() if x not in self.__TK_KWARGS}
        super().__init__(master=master, title=title, **kwargs)   #type: ignore
        self.bind('<Escape>', lambda _: self.destroy())
        # Устанавливаем геометрию окна до основной отрисовки
        self.set_geometry()
        self.main(**my_kwargs)   
        self.wait_visibility()
        self.focus_set()
        self.grab_set()
        
    def main(self, **kwargs) -> None:
        """Абстрактная ф-я для сборки других ф-й. Запускается в момент инициализации объекта.
        В основном, служит для сборки ф-й отрисовки дочерних виджетов."""
        pass

    def set_geometry(self) -> None:
        """Установка размеров окна и центрирование его относительно центрального"""
        width, height = self._geometry
        place_x = ((self.master.winfo_width() - width) // 2) + self.master.winfo_x()
        place_y = ((self.master.winfo_height() - height) // 2) + self.master.winfo_y()
        self.geometry(f"{width}x{height}+{place_x}+{place_y}")
        self.resizable(False, False)


def style_init():
    """Ф-я для инициализации общих используемых стилей. Вызывается после инициализации основного объекта ttkbootstrap."""
    style = tb.Style()
    style.configure('mini.Outline.TMenubutton', padding=(5, 1, 0, 1))
    style.configure('mini.dark.Outline.TMenubutton', padding=(5, 1, 0, 1))
    style.configure('db.TFrame', background='red')