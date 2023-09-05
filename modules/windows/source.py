import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd
from tkinter import colorchooser as tkcc


class MyButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, relief=tk.FLAT, fg="#eee", bg="#454545", **kwargs)


class ChildWindow(tk.Toplevel):
    """Конструктор для дочерних окон"""
    def __init__(self, parent_root):
        self.modules = parent_root.modules  # Сохраняем ссылку на модули программы
        super().__init__(master=parent_root)
        self.main()             # Абстрактная ф-я, которая собирает все виджеты дочернего окна
        self.resizable(False, False)
        self.to_parent_center()
        self.focus_set()
        self.grab_set()

    def main(self):
        """Абстрактная ф-я для сборки отрисовки виджетов наследуемых окон"""
        pass

    def to_parent_center(self):
        """Центрирование относительно родительского окна"""
        self.update_idletasks()
        place_x = ((self.master.winfo_width() - self.winfo_width()) // 2) + self.master.winfo_x()
        place_y = ((self.master.winfo_height() - self.winfo_height()) // 2) + self.master.winfo_y()
        self.geometry(f"+{place_x}+{place_y}")
