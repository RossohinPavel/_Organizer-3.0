import tkinter
import ttkbootstrap as tb
from typing import Callable, NamedTuple, Any, Mapping
from appmanager import AppManager


class Side(NamedTuple):
    width: int
    height: int


class ChildWindow(tb.Toplevel):
    """Конструктор для дочерних окон"""
    WIN_GEOMETRY = Side(100, 100)
    LIN_GEOMETRY = Side(100, 100)

    # 
    match AppManager.SYSTEM:
        case 'win': _geometry = WIN_GEOMETRY
        case 'lin' | _: _geometry = LIN_GEOMETRY

    #
    win_title = None

    #
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


# class TipWindow(tk.Toplevel):
#     """Конструктор окна всплывающих подсказок по клику мыши"""
#     _current_tip = None

#     def __init__(self, *args, **kwargs) -> None:
#         self.text = self.get_text(kwargs)
#         self.event = self.get_event(kwargs)
#         super().__init__(*args, **kwargs)
#         self.overrideredirect(True)
#         self.config(relief='solid', borderwidth=1)
#         self.bind('<ButtonPress>', lambda x: self.destroy())    # Бинд на закрытие при любой дейвствии
#         self.bind('<Escape>', lambda x: self.destroy())
#         self.bind('<FocusOut>', lambda x: self.destroy())
#         self.focus_set()
#         self.show_text()
#         self.set_position()

#     @staticmethod
#     def get_text(kwargs: dict) -> str | None:
#         """Получаем текст из kwargs"""
#         text = None
#         if "text" in kwargs:
#             return kwargs.pop('text')
#         return text

#     @staticmethod
#     def get_event(kwargs: dict) -> tk.Event | None:
#         """Получаем событие клика мыши"""
#         event = None
#         if "mouse_event" in kwargs:
#             return kwargs.pop('mouse_event')
#         return event

#     def set_position(self) -> None:
#         """Устанавливаем положение окна по координатам клика мыши. Сдвигаем по необходимости от края экрана"""
#         if not self.event:
#             return
#         x_pos, y_pos = self.event.x_root, self.event.y_root
#         self.update_idletasks()
#         x_shift = self.winfo_screenwidth() - x_pos - self.winfo_width()
#         y_shift = self.winfo_screenheight() - y_pos - self.winfo_height()
#         if x_shift < 0:
#             x_pos = x_pos + x_shift
#         if y_shift < 0:
#             y_pos = y_pos - y_shift
#         self.geometry(f'+{x_pos}+{y_pos}')

#     def show_text(self) -> None:
#         """Отображение текста на виджете"""
#         if not self.text:
#             return
#         tk.Label(master=self, text=self.text, bg='#FFFFE0', justify='left').pack(padx=1, pady=1)
