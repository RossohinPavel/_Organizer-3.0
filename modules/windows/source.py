import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd
from tkinter import colorchooser as tkcc


class LabeledFrame(ttk.Frame):
    def __init__(self, *args, text='', **kwargs):
        super().__init__(*args, padding=(4, 7, 4, 3), **kwargs)
        self.container = ttk.Frame(master=self, width=50, height=50, borderwidth=1, padding=(2, 6, 2, 2), relief='solid')
        self.container.pack(fill='both')
        ttk.Label(master=self, text=text).place(x=18, y=-9)


class MyButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, relief=tk.FLAT, fg="#eee", bg="#454545", **kwargs)


class ChildWindow(tk.Toplevel):
    """Конструктор для дочерних окон"""
    def __init__(self, parent_root):
        self.app_m = parent_root.app_m  # Сохраняем ссылку на модули программы
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
