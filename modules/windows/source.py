import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd


class ChildWindow(tk.Toplevel):
    """Конструктор для дочерних окон"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_m = self.master.app_m
        self.main()
        self.to_parent_center()
        self.focus_set()
        self.grab_set()

    def main(self):
        """Абстрактная ф-я для сборки отрисовки виджетов наследуемых окон"""
        pass

    def to_parent_center(self):
        """Центрирование относительно родительского окна"""
        self.resizable(False, False)
        self.master.update_idletasks()
        width, height = self.winfo_width(), self.winfo_height()
        place_x = ((self.master.winfo_width() - width) // 2) + self.master.winfo_x()
        place_y = ((self.master.winfo_height() - height) // 2) + self.master.winfo_y()
        self.geometry(f"{width}x{height}+{place_x}+{place_y}")


class MyButton(tk.Button):
    """Конструктор для кнопки с нужным стилем"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, relief=tk.FLAT, fg="#eee", bg="#454545", **kwargs)
