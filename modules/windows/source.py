import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd


class ChildWindow(tk.Toplevel):
    """Конструктор для дочерних окон"""
    width = 20
    height = 20

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Escape>', lambda x: self.destroy())
        self.set_geometry()
        self.app_m = getattr(self.master, 'app_m', None)
        self.main(*args, **kwargs)
        self.focus_set()
        self.grab_set()

    def main(self, *args, **kwargs):
        """Абстрактная ф-я для сборки других ф-й. Запускается в момент инициализации объекта.
        В основном, служит для сборки ф-й отрисовки дочерних виджетов."""
        pass

    def set_geometry(self):
        """Установка размеров окна и центрирование его относительно центрального"""
        place_x = ((self.master.winfo_width() - self.width) // 2) + self.master.winfo_x()
        place_y = ((self.master.winfo_height() - self.height) // 2) + self.master.winfo_y()
        self.geometry(f"{self.width}x{self.height}+{place_x}+{place_y}")
        self.resizable(False, False)


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
        self.bind('<FocusOut>', lambda x: self.destroy())
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


class LabeledFrame(ttk.Frame):
    """Конструктор для фрейма с надписью"""
    def __init__(self, *args, text='', **kwargs):
        super().__init__(*args, padding=(3, 7 if text else 3, 3, 3), **kwargs)
        self.container = ttk.Frame(master=self, borderwidth=1, padding=2, relief='solid')
        self.container.pack(fill='both', expand=1)
        if text:
            label = ttk.Label(master=self, text=text)
            label.place(x=20, y=-9)
            self.update_idletasks()
            self.container.config(width=label.winfo_width() + 25, height=label.winfo_height() - 8, padding=(2, 9, 2, 2))
