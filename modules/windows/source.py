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
