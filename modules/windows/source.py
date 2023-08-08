import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd
from tkinter import colorchooser as tkcc


class MyButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, relief=tk.FLAT, fg="#eee", bg="#454545", **kwargs)


class CellOneButton(tk.Frame):
    """Конструктор для одиночных кнопок"""
    def __init__(self, func_name='Название кнопки', func=None, pd_x=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button = MyButton(master=self, text=func_name, command=func, padx=pd_x)
        self.button.pack(pady=3, fill=tk.X, padx=8)

    def pack(self, *args, **kwargs):
        kwargs['padx'] = kwargs.get('padx', 60)
        super().pack(*args, fill=tk.X, **kwargs)


class CellTwoButton(tk.Frame):
    """Конструктор для парных кнопок"""
    def __init__(self, bt_l_name='Название', bt_l_func=None, bt_r_name='Название', bt_r_func=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.l_button = MyButton(self, text=bt_l_name, command=bt_l_func, width=15)
        self.l_button.pack(side=tk.LEFT, padx=8, pady=3)
        self.r_button = MyButton(self, text=bt_r_name, command=bt_r_func, width=15)
        self.r_button.pack(side=tk.RIGHT, padx=8, pady=3)


class ChildWindow(tk.Toplevel):
    """Конструктор для дочерних окон"""
    def __init__(self, parent_root):
        super().__init__(master=parent_root)
        self.settings = parent_root.settings    # Сохраняем ссылку на настройки
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
