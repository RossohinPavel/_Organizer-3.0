import ttkbootstrap as tb
from typing import Callable, NamedTuple, Any
from appmanager import AppManager


class Geometry(NamedTuple):    
    win: str
    lin: str


# class ChildWindow(ctk.CTkToplevel):
#     """Конструктор для дочерних окон"""
#     win_geometry: Geometry = Geometry('100x100', '100x100')
#     win_title = None

#     def __new__(cls, *args, **kwargs) -> Self:
#         if cls.win_title is None:       
#             cls.win_title = cls.__name__    # Задаем имя окна от класса, на основе которого оно создается.
#         return super().__new__(cls)

#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         self.title(self.win_title)
#         self.bind('<Escape>', lambda x: self.destroy())
#         self.set_geometry()             # Устанавливаем геометрию окна до основной отрисовки   
#         self.main(*args, **kwargs)   
#         self.wait_visibility()
#         self.focus_set()
#         self.grab_set()
        
#     def main(self, *args, **kwargs) -> None:
#         """Абстрактная ф-я для сборки других ф-й. Запускается в момент инициализации объекта.
#         В основном, служит для сборки ф-й отрисовки дочерних виджетов."""
#         pass

#     def set_geometry(self) -> None:
#         """Установка размеров окна и центрирование его относительно центрального"""
#         width, height = map(int, getattr(self.win_geometry, AppManager.SYSTEM).split('x'))
#         place_x = ((self.master.winfo_width() - width) // 2) + self.master.winfo_x()
#         place_y = ((self.master.winfo_height() - height) // 2) + self.master.winfo_y()
#         self.geometry(f"{width}x{height}+{place_x}+{place_y}")
#         self.resizable(False, False)


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
