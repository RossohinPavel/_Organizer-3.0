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
        self.parent_root = parent_root
        super().__init__(master=parent_root)
        self.geometry(f"+{self.parent_root.winfo_x()}+{self.parent_root.winfo_y()}")    # Предустановка в NW угол
        self.focus_set()
        self.grab_set()

    def to_parent_center(self):
        """Центрирование относительно родительского окна"""
        self.update_idletasks()
        parent_width = self.parent_root.winfo_width()  # Получаем размер родительского окна
        parent_height = self.parent_root.winfo_height()
        parent_place_x = self.parent_root.winfo_x()  # Получаем положение родительского окна
        parent_place_y = self.parent_root.winfo_y()
        child_width = self.winfo_width()  # Размер дочернего окна
        child_height = self.winfo_height()
        place_x = ((parent_width - child_width) // 2) + parent_place_x
        place_y = ((parent_height - child_height) // 2) + parent_place_y
        self.geometry(f"+{place_x}+{place_y}")
