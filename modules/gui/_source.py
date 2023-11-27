import tkinter
import ttkbootstrap as tb
from tkinter import messagebox as tkmb
from typing import Callable, NamedTuple, Any, Mapping, Type, Literal
from appmanager import AppManager


class Geometry(NamedTuple):
    """Для описании геометрии окон, фреймов и т.д."""
    width: int
    height: int


class ChildWindow(tb.Toplevel):
    """Конструктор для дочерних окон"""
    WIN_GEOMETRY = Geometry(100, 100)
    LIN_GEOMETRY = Geometry(100, 100)

    # Переменная для хранения имени окна
    win_title = None

    # Список обязательных атирбутов для инициализации tb.Toplevel
    __TK_KWARGS = (
        'title', 
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
        'alpha',
        'relief',
        'border'
        )
    
    def __init__(self, master: tkinter.Misc, /, **kwargs) -> None:
        kwargs.setdefault('title', self.win_title if self.win_title else self.__class__.__name__)
        # Фильтруем атрибуты, чтобы лишние не были переданы в инициализатор окна
        super().__init__(master=master, **{x: y for x, y in kwargs.items() if x in self.__TK_KWARGS})   #type: ignore
        self.bind('<Escape>', lambda _: self.destroy())
        # Устанавливаем геометрию окна до основной отрисовки
        self.set_window_geometry()
        self.main(**kwargs)   
        self.focus_set()
        self.grab_set()
        
    def main(self, **kwargs) -> None:
        """Абстрактная ф-я для сборки других ф-й. Запускается в момент инициализации объекта.
        В основном, служит для сборки ф-й отрисовки дочерних виджетов."""
        pass

    def get_geometry_by_system(self) -> Geometry:
        """Определяем тип ос и возвращаем соответствующую геометрию"""
        match AppManager.SYSTEM:     
            case 'win': return self.WIN_GEOMETRY
            case 'lin' | _: return self.LIN_GEOMETRY

    def set_window_geometry(self) -> None:
        """Установка размеров окна и центрирование его относительно центрального"""
        width, height = self.get_geometry_by_system()
        place_x = ((self.master.winfo_width() - width) // 2) + self.master.winfo_x()
        place_y = ((self.master.winfo_height() - height) // 2) + self.master.winfo_y()
        self.geometry(f"{width}x{height}+{place_x}+{place_y}")
        self.resizable(False, False)
        self.update_idletasks()


def style_init():
    """Ф-я для инициализации общих используемых стилей. Вызывается после инициализации основного объекта ttkbootstrap."""
    style = tb.Style()
    # Стиль миникнопок - менюшек
    style.configure(
        'mini.Outline.TMenubutton', 
        padding=(5, 1, 0, 1),
        )
    # Отладочный стиль для Frame
    style.configure(
        'db.TFrame', 
        background='red'
        )