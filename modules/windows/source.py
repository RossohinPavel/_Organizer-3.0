import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd


class ChildWindow(tk.Toplevel):
    """Конструктор для дочерних окон"""
    width = 1
    height = 1

    def __init__(self, *args, **kwargs):
        self.do_before(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.bind('<Escape>', lambda x: self.destroy())
        self.set_geometry()
        self.app_m = self.master.app_m
        self.do_after(*args, **kwargs)
        self.focus_set()
        self.grab_set()

    def do_before(self, *args, **kwargs):
        """Абстрактная ф-я для сборки других ф-й, которые делают что-то до вызова виджета"""
        pass

    def set_geometry(self):
        """Установка размеров окна и центрирование его относительно центрального"""
        place_x = ((self.master.winfo_width() - self.width) // 2) + self.master.winfo_x()
        place_y = ((self.master.winfo_height() - self.height) // 2) + self.master.winfo_y()
        self.geometry(f"{self.width}x{self.height}+{place_x}+{place_y}")
        self.resizable(False, False)

    def do_after(self, *args, **kwargs):
        """Абстрактная ф-я для сборки других ф-й, которые делают что-то после вызова виджета"""
        pass


class MyButton(tk.Button):
    """Конструктор для кнопки с нужным стилем"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, relief=tk.FLAT, fg="#eee", bg="#454545", **kwargs)


class TipWindow(tk.Toplevel):
    """Конструктор окна всплывающих подсказок по клику мыши"""
    _current_tip = None

    def __init__(self, *args, **kwargs):
        self.text = self.get_text(kwargs)
        self.event = self.get_event(kwargs)
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        self.bind('<ButtonPress>', lambda x: self.destroy())
        self.bind('<Escape>', lambda x: self.destroy())
        self.focus_set()
        self.set_position()
        self.show_text()

    @staticmethod
    def get_text(kwargs: dict):
        """Получаем текст из kwargs"""
        text = None
        if "text" in kwargs:
            return kwargs.pop('text')
        return text

    @staticmethod
    def get_event(kwargs: dict):
        """Получаем событие клика мыши"""
        event = None
        if "mouse_event" in kwargs:
            return kwargs.pop('mouse_event')
        return event

    def set_position(self):
        """Устанавливаем положение окна по координатам клика мыши"""
        if not self.event:
            return
        self.geometry(f'+{self.event.x_root}+{self.event.y_root}')

    def show_text(self):
        """Отображение текста на виджете"""
        if not self.text:
            return
        tk.Label(master=self, text=self.text, bg='#FFFFE0', relief='raised', justify='left').pack(padx=1, pady=1)
